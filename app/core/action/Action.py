class Action():

    instance = None

    REQUEST_MODULE_KEY = "module"
    REQUEST_ACTION_KEY = "action"

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

            module = jsonData[Action.REQUEST_MODULE_KEY].upper()
            action = jsonData[Action.REQUEST_ACTION_KEY].upper()

            handler = self._getHandler(module, action)
            
            if handler is None:
                return self.createBadRequestResponse(
                    jsonData, 
                    "No handler for request was found!"
                )

            response = handler.request(jsonData)

            if 'status' not in response:
                response["status"] = 200

            response[Action.REQUEST_MODULE_KEY] = module
            response[Action.REQUEST_ACTION_KEY] = action

            return response

        except Exception as e:
            return self.createErrorResponse(jsonData, e)
    
    def _getHandler(self, module, action):
        pass

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
    
    