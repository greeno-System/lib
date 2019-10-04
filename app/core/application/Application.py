import os
import os.path
from ctypes import cdll, byref, create_string_buffer
from lib.app.core.config.Config import Config
from lib.app.system.ApplicationStatusObserver import ApplicationStatusObserver
from lib.app.equipment.EquipmentCollection import EquipmentCollection


class Application():

    app = None

    @staticmethod
    def app():
        return Application.app

    def __init__(self, configFilePath):
        Application.app = self
        self.config = self._createConfig(configFilePath)

        statusFile = os.getcwd() + "/../APPLICATION_STATUS"
        self.statusObserver = ApplicationStatusObserver(self, statusFile)

    def start(self):
        self._setProcessName(self.config.get("applicationProcess"))
        self.statusObserver.start()

        return

        self.equipmentCollection = self._createEquipmentCollection()
        self.loadEquipment(self.equipmentCollection)

    def _setProcessName(self, processName):

        if processName == None or not processName:
            raise ValueError("Cannot set name of application process. No process name given!")

        processName = processName.strip()

        libc = cdll.LoadLibrary('libc.so.6')
        buff = create_string_buffer(len(processName)+1)
        buff.value = bytes(processName, "UTF-8")
        libc.prctl(15, byref(buff), 0, 0, 0)

    def _createConfig(self, configFilePath):

        if not configFilePath:
            raise ValueError("no file path for application config given!")

        if not os.path.isfile(configFilePath):
            raise FileNotFoundError("Configuration file does not exist at' " + configFilePath + "'")

        config = Config(configFilePath)

        return config
    
    def _createEquipmentCollection(self):
        file = self.config.get("equipmentFilePath")

        return EquipmentCollection(file)

    def loadEquipment(self, collection):
        if not collection:
            raise ValueError("No equipment collection given!")

        #TODO: load equipment

    def getStatusObserver(self):
        return self.statusObserver

    def stop(self):
        pass

    def reload(self):
        pass