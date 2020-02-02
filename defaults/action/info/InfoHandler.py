from lib.app.core.action.ActionHandler import ActionHandler
from lib.app.core.action.Action import Action
from lib.app.core.application.Application import Application

class InfoHandler(ActionHandler):

    def request(self, jsonData):

        response = self.createResponse()

        config = Application.app().getSystemConfig()
        dataKey = Action.REQUEST_DATA_KEY

        data = {
            'name': config.get("name"),
            'version': config.get("version")
        }

        response[dataKey] = data

        return response