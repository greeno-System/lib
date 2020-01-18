import os.path
from lib.app.core.config.Config import Config
import importlib
class Action():

    # singleton instance
    instance = None

    # constants for request and response keys
    REQUEST_MODULE_KEY = "module"
    REQUEST_ACTION_KEY = "action"
    REQUEST_DATA_KEY = "data"
    RESPONSE_STATUS_KEY = "status"

    # constants for response status
    STATUS_OK = 200
    STATUS_BAD_REQUEST = 400
    STATUS_NO_RESPONSE = 444
    STATUS_ERROR = 500

    # relative path of directory which contains the core action handlers
    CORE_HANDLER_DIRECTORY = "lib/defaults/action/"

    # returns the instance of the singleton
    @classmethod
    def getInstance(self):
        if Action.instance is None:
            Action.instance = Action()

        return Action.instance

    # constructor
    def __init__(self):
        self.handlers = {}

        from lib.app.core.application.Application import Application
        self.logger = Application.app().getLogger()


    # main function for a request to application
    # searches for a suitable action handler
    # return response from handler or in case of an error a generated one
    def request(self, jsonData):
        try:

            if (Action.REQUEST_MODULE_KEY not in jsonData) or (Action.REQUEST_ACTION_KEY not in jsonData):
                return self.createBadRequestResponse(
                    jsonData,
                    "Module or action parameter is missing."
                )

            module = jsonData[Action.REQUEST_MODULE_KEY].lower()
            action = jsonData[Action.REQUEST_ACTION_KEY].lower()

            handler = self._getHandler(module, action)
            
            if handler is None:
                return self.createBadRequestResponse(
                    jsonData, 
                    "Could not find a suitable handler for request!"
                )

            response = handler.request(jsonData)

            if response is None or not response:
                return self.createNoResponseResponse(jsonData, "Handler did not send response.")

            if 'status' not in response:
                response["status"] = Action.STATUS_OK

            response[Action.REQUEST_MODULE_KEY] = module
            response[Action.REQUEST_ACTION_KEY] = action

            return response

        except Exception as e:
            self.logger.error(e)
            return self.createErrorResponse(jsonData, "An error occured on your device.")
    
    # helper function to get registered action handler for module and action
    # returns None if no suitable handler was registered
    def _getHandler(self, module, action):
        
        if module not in self.handlers:
            return None

        if action not in self.handlers[module]:
            return None

        return self.handlers[module][action]

    # creates an action handler instance from given installation path
    def createHandler(self, installationPath, moduleName):

        if moduleName is None or not moduleName:
            raise ValueError("Module name for action handler is missing!")

        configFile = installationPath + "/action.xml"

        if not os.path.isfile(configFile):
            raise FileNotFoundError("Action handler file does not exist at '" + configFile + "'")

        config = Config(configFile)
        name = config.get("name")
        className = config.get("className")

        package = (installationPath.strip("/") + "/" + className).replace("/", ".")
        handlerClass = getattr(importlib.import_module(package), className)

        return handlerClass(moduleName, name)

    # registers an action handler instance with its module name and its action name
    def registerHandler(self, actionHandler):
        moduleName = actionHandler.getModule().lower()
        name = actionHandler.getAction().lower()

        if moduleName not in self.handlers:
            self.handlers[moduleName] = {}

        self.handlers[moduleName][name] = actionHandler

    # creates a response from request data with bad request status
    def createBadRequestResponse(self, jsonData, message):

        if Action.REQUEST_MODULE_KEY in jsonData:
            module = jsonData[Action.REQUEST_MODULE_KEY]
        else:
            module = "unknown"

        if Action.REQUEST_ACTION_KEY in jsonData:
            action = jsonData[Action.REQUEST_ACTION_KEY]
        else:
            action = "unknown"

        return {
            'status': Action.STATUS_BAD_REQUEST,
            'module': module,
            'action': action,
            'data': {
                'message': message
            }
        }

    # creates a response from request data with error status
    def createErrorResponse(self, jsonData, message):

        module = jsonData[Action.REQUEST_MODULE_KEY]
        action = jsonData[Action.REQUEST_ACTION_KEY]

        return {
            'status': Action.STATUS_ERROR,
            'module': module,
            'action': action,
            'data': {
                'message': message
            }
        }
    
    # creates a response from request data with no response status
    def createNoResponseResponse(self, jsonData, message):
        module = jsonData["module"]
        action = jsonData["action"]

        return {
            'status': Action.STATUS_NO_RESPONSE,
            'module': module,
            'action': action,
            'data': {
                'message': message
            }
        }
    