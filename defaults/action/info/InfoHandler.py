from lib.app.core.action.ActionHandler import ActionHandler
from lib.app.core.action.Action import Action
from lib.app.core.application.Application import Application

class InfoHandler(ActionHandler):

    def request(self, jsonData):

        response = self.createResponse()

        response[Action.REQUEST_DATA_KEY]["version"] = Application.app().config.get("version")
        
        return response