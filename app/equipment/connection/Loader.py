from lib.app.equipment.EquipmentLoader import EquipmentLoader
from lib.app.core.config.Config import Config
import os.path

class ConnectionLoader(EquipmentLoader):

    def test(self):
        print("hello from connection loader!")

    def loadComponent(self, installationPath):
        
        config = self._createConnectionConfig(installationPath)

    def isLoadable(self):
        pass

    def _createConnectionConfig(self, installationPath):
        configFile = installationPath + "connection.xml"

        if not os.path.isfile(configFile):
            raise FileNotFoundError("Configuration file not found at '" + configFile + "'")

        return Config(configFile)