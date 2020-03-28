from abc import ABC
from abc import abstractmethod
from lib.app.core.action.Action import Action

class DataInterface(ABC):

    def __init__(self, config = False):

        self.config = config
        self.action = Action.getInstance()

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    def request(self, jsonData):

        if jsonData is None:
            raise ValueError("No JSON Request found!")

        return self.action.request(jsonData).getJSON()