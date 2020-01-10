from lib.app.core.action.ActionHandler import ActionHandler
from lib.app.core.action.Action import Action
from lib.app.core.application.Application import Application

class InfoHandler(ActionHandler):

    def request(self, jsonData):

        return {
            Action.REQUEST_MODULE_KEY: self.getModule(),
            Action.REQUEST_ACTION_KEY: self.getAction(),
            Action.RESPONSE_STATUS_KEY: Action.STATUS_OK,
            Action.REQUEST_DATA_KEY: {
                "version": Application.app().config.get("version")
            }
        }