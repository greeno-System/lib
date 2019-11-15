from lib.app.equipment.connection.Connection import Connection
from abc import ABC
from abc import abstractmethod
from lib.app.equipment.connection.MultiChannelConnectionConfigReader import MultiChannelConnectionConfigReader

class MultiChannelConnection(Connection, ABC):

    def _createConfigReader(self):
        return MultiChannelConnectionConfigReader()

    @abstractmethod
    def createChannel(self):
        pass