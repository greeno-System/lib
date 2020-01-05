import os
import os.path
import logging
import sys
from ctypes import cdll, byref, create_string_buffer
from lib.app.core.config.Config import Config
from lib.app.core.application.SystemConfigReader import SystemConfigReader
from lib.app.system.ApplicationStatusObserver import ApplicationStatusObserver
from lib.app.equipment.EquipmentSet import EquipmentSet
from lib.app.equipment.Equipment import Equipment
from lib.app.core.action.Action import Action

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

        self.action = Action.getInstance()
        self.registerActionHandlers()

        self.equipment = self._createEquipment()
        self.equipment.loadEquipment()

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

        config = Config(configFilePath, SystemConfigReader())

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

    def registerActionHandlers(self):

        for item in os.listdir(Action.CORE_HANDLER_DIRECTORY):

            installationDir = Action.CORE_HANDLER_DIRECTORY + item
            handler = self.action.createHandler(installationDir, "core")

            self.action.registerHandler(handler)
    
    def _createEquipment(self):

        setFile = os.getcwd() + "/equipment.xml"

        return Equipment(EquipmentSet(setFile))

    def stop(self):
        self.equipment.deloadEquipment()

    def reload(self):
        pass

    def getStatusObserver(self):
        return self.statusObserver

    def Equipment(self):
        return self.equipment

    def Action(self):
        return self.action

    def getLogger(self):
        return self.logger