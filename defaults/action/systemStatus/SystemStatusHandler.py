from lib.app.core.action.ActionHandler import ActionHandler

class SystemStatusHandler(ActionHandler):

    def request(self, jsonData):
        print("got Request!")