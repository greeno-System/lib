from abc import ABC
from abc import abstractmethod

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