from abc import ABC
from abc import abstractmethod

class ConnectionFactory(ABC):

    def __init__(self, configFile):
        pass

    @abstractmethod
    def createConnection(self, config):
        pass