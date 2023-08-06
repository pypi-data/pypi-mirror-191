from .Job import Job
from .Preset import Preset
from time import sleep,time
import urllib.parse
import json
import redis
from .functions import *
class SupplyChain:

    def __init__(self,Asset,id=None,name=None):
        if not id and not name:
            raise TypeError("Please specify either the name or id of the rule that starts the supply chain")
        self.Rally = Asset.Rally
        self.Asset = Asset
        self.id = id
        self.name = name
        self.baseWorkflow = None
        self.jobs = []
        if not id:
            try:
                self.id = self.Rally.apiCall("GET","/workflowRules?filter=name={}".format(urllib.parse.quote_plus(name)))["data"][0]["id"]
            except IndexError:
                raise ValueError("Could not find rule with name '{}'".format(name)) from None

    def run(self,initData={},endingPresetName=None,endingPresetId=None,timeout=15,protectProd=True):
        if not any([silo in self.Rally.apiUrl for silo in ["dev","qa","uat"]]) and protectProd:
            raise ValueError("Production assets are read only") from None
        if endingPresetName and not endingPresetId:
            endingPresetId = self.Asset.preset(name=endingPresetName).id
        self.Asset.updateTestModeState(True)
        self.baseWorkflow = self.Rally.apiCall("POST","/workflows",body={"data":{"type":"workflows", "attributes":{"initData":json.dumps(initData)}, "relationships": {"movie":{"data":{"id": self.Asset.id,"type": "movies",}},"workflowRule":{"data": {"id": self.id, "type": "workflowRules",}}}}})["data"]
        workflows = [self.baseWorkflow]
        if self.Rally.redisUrl:
            redisClient = redis.Redis.from_url(url=self.Rally.redisUrl,ssl_cert_reqs=None)
            subscriber = redisClient.pubsub(ignore_subscribe_messages=True)
            subscriber.subscribe('messagebus')
            start_time = time()
            delay = 0.1
            while (time() - start_time < timeout):
                response = subscriber.get_message()
                if response:
                    data = json.loads(response["data"])
                    attributes = jsonPath(data,"resourceState.data.attributes") or {}
                    relationships = jsonPath(data,"resourceState.data.relationships") or {}
                    result = attributes.get("result")
                    isComplete = result != None
                    if data["resourceType"] == "workflows":
                        baseWorkflowId = jsonPath(relationships,"baseWorkflow.data.id")
                        assetId = jsonPath(relationships,"asset.data.id")
                        if self.baseWorkflow["id"] == data["resourceId"] and isComplete:
                            break
                        elif assetId == self.Asset.id and baseWorkflowId == self.baseWorkflow["id"]:
                            workflows.append(jsonPath(data,"resourceState.data"))
                            workflows = list({v["id"]:v for v in workflows}.values())
                    elif data["resourceType"] == "jobs":
                        workflowId = jsonPath(relationships,"workflow.data.id")
                        isAssociatedWorkflow = workflowId in [i["id"] for i in workflows]
                        if isAssociatedWorkflow and isComplete:
                            if endingPresetId == jsonPath(relationships,"preset.data.id"):
                                break
                sleep(delay)
            subscriber.unsubscribe()
        else:
            delay = 5
            start_time = time()
            while (time() - start_time < timeout):
                sleep(delay)
                self.baseWorkflow = self.Rally.apiCall("GET","/workflows/{}".format(self.baseWorkflow["id"]))["data"]
                if self.baseWorkflow["attributes"]["result"] != None:
                    break
                if endingPresetId:
                    for workflow in self.getAllWorkflows():
                        endingPresetJob = self.Rally.apiCall("GET","/jobs?filter=workflowId={},presetId={}".format(workflow["id"],endingPresetId),paginate=True)["data"]
                        if len(endingPresetJob) != 0:
                            if endingPresetJob[0]["attributes"]["result"] != None:
                                break
                    else:
                        continue
                    break
        self.end()
        self.Asset.updateTestModeState(None)
        return self.jobs

    def end(self):
        if self.baseWorkflow:
            while self.baseWorkflow["attributes"]["result"] == None:
                for workflow in self.getAllWorkflows():
                    workflow_jobs = [i["id"] for i in self.Rally.apiCall("GET","/workflows/{}".format(workflow["id"]))["data"]["relationships"]["jobs"]["data"]]
                    for workflow_job in workflow_jobs:
                        job_data = self.Rally.apiCall("GET","/jobs/{}".format(workflow_job))["data"]
                        preset = Preset(self.Asset,id=jsonPath(job_data,"relationships.preset.data.id"))
                        job = Job(preset,id=job_data["id"],attributes=job_data["attributes"])
                        if job.result != None and job.state != "Cancelled":
                            self.addJob(job)
                        else:
                            job.cancel()
                self.baseWorkflow = self.Rally.apiCall("GET","/workflows/{}".format(self.baseWorkflow["id"]))["data"]

    def getAllWorkflows(self):
        if self.baseWorkflow:
            workflows = [self.baseWorkflow]
            childWorkflows = [item for item in self.Rally.apiCall("GET","/workflows?filter=assetId={}".format(self.Asset.id),paginate=True)["data"] if item["relationships"]["baseWorkflow"]["data"]["id"] == self.baseWorkflow["id"] and item["id"] != self.baseWorkflow["id"]]
            workflows.extend(childWorkflows)
            return workflows

    def addJob(self,job):
        newJob = True
        for i in range(len(self.jobs)):
            if self.jobs[i].id == job.id:
                self.jobs[i] = job
                newJob = False
        if newJob:
            self.jobs.append(job)