from lib.app.equipment.EquipmentLoader import EquipmentLoader
from lib.app.core.config.Config import Config
import os.path
import importlib

class ConnectionLoader(EquipmentLoader):

    def createComponent(self, installationPath):

        config = self._createConnectionConfig(installationPath)

        className = config.get("class")
        package = (installationPath + className).replace("/", ".")

        connectionClass = getattr(importlib.import_module(package), className)

        connection = connectionClass()

        return connection

    def _createConnectionConfig(self, installationPath):
        configFile = installationPath + "/connection.xml"

        if not os.path.isfile(configFile):
            raise FileNotFoundError("Configuration file not found at '" + configFile + "'")

        return Config(configFile)

    def loadComponent(self, component):
        component.open()

    def deloadComponent(self, connection):

        try:
            if connection is not None:
                connection.close()
        except Exception as e:
            self.logger.error(e)