from lib.app.equipment.EquipmentLoader import EquipmentLoader
import os.path
from lib.app.core.config.Config import Config
import importlib

class DataInterfaceLoader(EquipmentLoader):

    def createComponent(self, installationPath):
        config = self._createConfig(installationPath)

        className = config.get("class")
        package = (installationPath + className).replace("/", ".")

        interfaceClass = getattr(importlib.import_module(package), className)
        
        interface = interfaceClass()

        return interface

    def loadComponent(self, component):
        component.open()


    def deloadComponent(self, dataInterface):
        dataInterface.close()

    def _createConfig(self, installationPath):

        configFile = installationPath + "/data_interface.xml"

        if not os.path.isfile(configFile):
            raise FileNotFoundError("Configuration file not found at '" + configFile + "'")

        return Config(configFile)

