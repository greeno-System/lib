from lib.app.core.action.ActionHandler import ActionHandler
from lib.app.core.action.Action import Action
from lib.app.core.application.Application import Application

from time import gmtime, strftime
from datetime import datetime

class InfoHandler(ActionHandler):

    def request(self, jsonData):

        response = self.createResponse()

        config = Application.app().config
        dataKey = Action.REQUEST_DATA_KEY

        data = {
            'name': config.get('name'),
            'version': config.get('version'),
            'time': datetime.now().strftime("%d.%m.%Y %H:%M")
        }

        response[dataKey] = data
        

        return response