from abc import ABC
from abc import abstractmethod
from lib.app.core.action.Action import Action

class ActionHandler(ABC):

    def __init__(self, module, action):
        self.module = module.lower()
        self.action = action.lower()

    @abstractmethod
    def request(self, jsonData):
        pass

    def getModule(self):
        return self.module

    def getAction(self):
        return self.action

    def createResponse(self):

        return {
            Action.REQUEST_MODULE_KEY: self.getModule(),
            Action.REQUEST_ACTION_KEY: self.getAction(),
            Action.REQUEST_DATA_KEY: {}
        }