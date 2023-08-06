def jsonPath(obj,pathString):
    pathParts = pathString.split(".")
    for index,pathPart in enumerate(pathParts):
        if index != (len(pathParts) - 1):
            obj = obj.get(pathPart,{}) or {}
        else:
            obj = obj.get(pathPart)
    return obj