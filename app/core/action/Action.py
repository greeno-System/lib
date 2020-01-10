import os.path
from lib.app.core.config.Config import Config
import importlib
class Action():

    instance = None

    REQUEST_MODULE_KEY = "module"
    REQUEST_ACTION_KEY = "action"
    REQUEST_DATA_KEY = "data"

    CORE_HANDLER_DIRECTORY = "lib/defaults/action/"

    def __init__(self):
        self.handlers = {}

    @classmethod
    def getInstance(self):
        if Action.instance is None:
            Action.instance = Action()

        return Action.instance

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
                    "No handler for request was found!"
                )

            response = handler.request(jsonData)

            if response is None or not response:
                return self.createNoResponseResponse(jsonData, "Handler did not send response.")

            if 'status' not in response:
                response["status"] = 200

            response[Action.REQUEST_MODULE_KEY] = module
            response[Action.REQUEST_ACTION_KEY] = action

            return response

        except Exception as e:
            return self.createErrorResponse(jsonData, e)
    
    def _getHandler(self, module, action):
        
        if module not in self.handlers:
            return None

        if action not in self.handlers[module]:
            return None

        return self.handlers[module][action]

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

    def registerHandler(self, actionHandler):
        moduleName = actionHandler.getModule().lower()
        name = actionHandler.getAction().lower()

        if moduleName not in self.handlers:
            self.handlers[moduleName] = {}

        self.handlers[moduleName][name] = actionHandler

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
            'status': 400,
            'module': module,
            'action': action,
            'data': {
                'message': message
            }
        }

    def createErrorResponse(self, jsonData, message):

        module = jsonData[Action.REQUEST_MODULE_KEY]
        action = jsonData[Action.REQUEST_ACTION_KEY]

        return {
            'status': 500,
            'module': module,
            'action': action,
            'data': {
                'message': message
            }
        }
    
    def createNoResponseResponse(self, jsonData, message):
        module = jsonData["module"]
        action = jsonData["action"]

        return {
            'status': 444,
            'module': module,
            'action': action,
            'data': {
                'message': message
            }
        }
    