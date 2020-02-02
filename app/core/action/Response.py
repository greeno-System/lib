
class Response():

    STATUS_OK = 200
    STATUS_BAD_REQUEST = 400
    STATUS_NO_RESPONSE = 444
    STATUS_ERROR = 500

    STATUS_LIST = [200, 400, 444, 500]

    # constructor
    def __init__(self, module=None, action=None, data=[]):

        if module is None:
            raise ValueError("Module parameter cannot be None!")

        if action is None:
            raise ValueError("Action parameter cannot be None!")

        self.module = module.strip().lower()
        self.action = action.strip().lower()

        self.data = data

        self.status = Response.STATUS_OK

    # returns the module
    def getModule(self):
        return self.module

    # returns the action
    def getAction(self):
        return self.action
    
    # sets the data for response
    def setData(self, data = []):
        self.data = data

    # returns the response data
    def getData(self):
        return self.data

    #sets the status for response
    def setStatus(self, status):
        
        if not status in Response.STATUS_LIST:
            raise ValueError("Status '" + str(status) + "' is not available!")
        
        self.status = status

    # returns the current status of the reponse
    def getStatus(self):
        return self.status

    # converts the response to JSON
    def getJSON(self):

        return {
            'module': self.module,
            'action': self.action,
            'status': self.status,
            'data': self.data
        }