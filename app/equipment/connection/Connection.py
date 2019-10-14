from abc import ABC
from abc import abstractmethod
import os.path
from lib.app.equipment.connection.ConnectionConfigReader import ConnectionConfigReader

class Connection(ABC):

    def __init__(self, params):

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def write(self, channel):
        pass

    @abstractmethod
    def read(self, channel):
        pass

