from abc import ABC
from abc import abstractmethod
import os.path
from lib.app.equipment.connection.ConnectionConfigReader import ConnectionConfigReader

class Connection(ABC):

    def __init__(self, installationPath):

        if not installationPath:
            raise ValueError("No installationPath given!")

        configFile = installationPath + "/connection.xml"

        self.config = self._createConfig(configFile)
        


    def _createConfig(self, configFile):

        if not os.path.isfile(configFile):
            raise FileNotFoundError("No connection configuration found. 'connection.xml' missing in '" + installationPath + "'")

        reader = self._createConfigReader()
        extend = self._isConfigReaderExtending()

        config = Config(configFile, reader, extend)

        return config

    def _createConfigReader(self):
        return ConnectionConfigReader()

    def _isConfigReaderExtending(self):
        return False

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

