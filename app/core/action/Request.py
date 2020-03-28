class Request():

    #converts json to a request object
    @staticmethod
    def fromJSON(jsonData = {}):

        if 'module' not in jsonData:
            jsonData["module"] = "core"

        module = jsonData["module"]

        if 'action' not in jsonData:
            raise RuntimeError("Request does not contain an action!") 

        action = jsonData["action"]

        if "data" in jsonData:
            return Request(module, action, jsonData["data"])
        else:
            return Request(module, action)

    # constructor
    def __init__(self, module="core", action=None, data=[]):

        if action is None:
            raise ValueError("Action parameter cannot not be None!")

        self.module = module.strip().lower()
        self.action = action.strip().lower()
        self.data = data

    # returns the destination module of the request
    def getModule(self):
        return self.module

    # returns the destination action of the request
    def getAction(self):
        return self.action

    # sets the data of the request
    def setData(self, data = []):
        self.data = data

    # returns the data of the request
    def getData(self):
        return self.data

    # converts the request into a json object
    def getJson(self):

        return {
            'module': self.module,
            'action': self.action,
            'data': self.data
        }