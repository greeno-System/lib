import os
import os.path
import logging
import sys
from ctypes import cdll, byref, create_string_buffer
from lib.app.core.config.Config import Config
from lib.app.system.ApplicationStatusObserver import ApplicationStatusObserver
from lib.app.equipment.EquipmentCollection import EquipmentCollection
from lib.app.equipment.EquipmentManager import EquipmentManager


class Application():

    application = None

    @staticmethod
    def app():
        return Application.application

    def __init__(self, configFilePath):

        if Application.application is not None:
            raise RuntimeError("An application instance does already exist!")

        Application.application = self

        self.config = self._createConfig(configFilePath)

        self.logger = self._createLogger(self.config)

        self._setProcessName(self.config.get("applicationProcess"))
        statusFile = os.getcwd() + "/../APPLICATION_STATUS"
        self.statusObserver = ApplicationStatusObserver(self, statusFile)
        self.statusObserver.start()

    def start(self):

        self.equipmentManager = self._createEquipmentManager()
        self.equipmentManager.loadEquipment()

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

    def _createLogger(self, config):

        if config is None:
            return False

        processName = config.get("applicationProcess")

        if processName is None or processName.strip() == "":
            return False

        logger = logging.getLogger(processName)
        logger.setLevel(logging.DEBUG)

        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        streamHandler.setFormatter(formatter)

        logger.addHandler(streamHandler)
        logger.propagate = False

        return logger
    
    def _createEquipmentManager(self):

        file = os.getcwd() + "/../equipment.xml"
        self.equipmentCollection = EquipmentCollection(file)

        return EquipmentManager(self.equipmentCollection)

        #TODO: load equipment

    def stop(self):
        pass

    def reload(self):
        pass

    def getStatusObserver(self):
        return self.statusObserver

    def getEquipmentManager(self):
        return self.equipmentManager

    def getLogger(self):
        return self.logger