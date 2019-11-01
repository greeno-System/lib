from abc import ABC
from abc import abstractmethod
import os.path
from lib.app.equipment.connection.ConnectionConfigReader import ConnectionConfigReader
from lib.app.core.application.Application import Application

class Connection(ABC):

    def __init__(self):
        self.logger = Application.app().getLogger()

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

