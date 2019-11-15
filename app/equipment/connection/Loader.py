from lib.app.equipment.EquipmentLoader import EquipmentLoader
from lib.app.core.config.Config import Config
import os.path
import importlib

class ConnectionLoader(EquipmentLoader):

    def loadComponent(self, installationPath):

        try:
            config = self._createConnectionConfig(installationPath)

            className = config.get("class")
            package = (installationPath + className).replace("/", ".")

            connectionClass = getattr(importlib.import_module(package), className)

            connection = connectionClass()
            connection.open()

            return connection

        except Exception as e:
            self.logger.error(e)

            return None

    def _createConnectionConfig(self, installationPath):
        configFile = installationPath + "connection.xml"

        if not os.path.isfile(configFile):
            raise FileNotFoundError("Configuration file not found at '" + configFile + "'")

        return Config(configFile)

    def deloadComponent(self, connection):

        try:
            if connection is not None:
                connection.close()
        except Exception as e:
            self.logger.error(e)