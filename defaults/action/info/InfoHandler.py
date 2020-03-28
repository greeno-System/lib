from lib.app.core.action.ActionHandler import ActionHandler
from lib.app.core.application.Application import Application

class InfoHandler(ActionHandler):

    def request(self, request, response):

        config = Application.app().getSystemConfig()

        data = {
            'name': config.get("name"),
            'version': config.get("version")
        }

        response.setData(data)

        return response