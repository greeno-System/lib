import os
import os.path
import logging
import sys
import signal
from ctypes import cdll, byref, create_string_buffer
from lib.app.core.config.Config import Config
from lib.app.core.application.SystemConfigReader import SystemConfigReader
from lib.app.core.application.AppConfigReader import AppConfigReader
from lib.app.system.ApplicationStatusObserver import ApplicationStatusObserver
from lib.app.equipment.EquipmentSet import EquipmentSet
from lib.app.equipment.Equipment import Equipment
from lib.app.core.action.Action import Action

class Application():

    # the static application instance
    application = None

    # static method to get application instance
    @staticmethod
    def app():
        return Application.application

    # constructor
    def __init__(
        self, 
        systemFile = "system.xml", 
        applicationFile = "app.xml",
    ):

        if Application.application is not None:
            raise RuntimeError("An application instance does already exist!")

        Application.application = self

        self.systemConfig = self._createSystemConfig(systemFile)
        self.appConfig = self._createAppConfig(applicationFile)
        self.equipmentFile = self.appConfig.get('paths')["equipmentSet"]

        self.logger = self._createLogger(self.systemConfig)

        self._setProcessName(self.systemConfig.get("applicationProcess"))

        statusFile = self.appConfig.get("paths")["systemStatus"]

        self.statusObserver = ApplicationStatusObserver(self, statusFile)
        self.statusObserver.start()

    #starts the application and does main functionality
    def start(self):
        self.equipment = self._createEquipment()
        self.equipment.loadEquipment()

        self.action = Action.getInstance()
        self.registerActionHandlers()

    # helper function to change the name of the python process
    def _setProcessName(self, processName):

        if processName == None or not processName:
            raise ValueError("Cannot set name of application process. No process name given!")

        processName = processName.strip()

        libc = cdll.LoadLibrary('libc.so.6')
        buff = create_string_buffer(len(processName)+1)
        buff.value = bytes(processName, "UTF-8")
        libc.prctl(15, byref(buff), 0, 0, 0)

    # creates a config object parsed from given file for system information
    def _createSystemConfig(self, configFilePath):

        if not configFilePath:
            raise ValueError("no file path for system config given!")

        if not os.path.isfile(configFilePath):
            raise FileNotFoundError("Configuration file does not exist at' " + configFilePath + "'")

        config = Config(configFilePath, SystemConfigReader())

        return config

    def _createAppConfig(self, configFilePath):
        if not configFilePath:
            raise ValueError("no file path for app config given!")

        if not os.path.isfile(configFilePath):
            raise FileNotFoundError("Configuration file does not exist at' " + configFilePath + "'")

        return Config(configFilePath, AppConfigReader())

    # creates the main logger object for the application
    def _createLogger(self, config):

        if config is None:
            return False

        processName = config.get("applicationProcess")

        if processName is None or processName.strip() == "":
            return False

        logger = logging.getLogger(processName)
        streamHandler = logging.StreamHandler()

        if self.isDebugMode(): 
            logger.setLevel(logging.DEBUG)
            streamHandler.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
            streamHandler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        streamHandler.setFormatter(formatter)

        logger.addHandler(streamHandler)
        logger.propagate = False

        return logger

    # registers core action handlers from lib and application
    def registerActionHandlers(self):

        for item in os.listdir(Action.CORE_HANDLER_DIRECTORY):

            installationDir = Action.CORE_HANDLER_DIRECTORY + item
            handler = self.action.createHandler(installationDir, "core")

            self.action.registerHandler(handler)

        customPath = self.appConfig.get("paths")["actionHandlers"].strip("/")

        if not os.path.isdir(customPath):
            raise ValueError("Could not find a directory for action handlers at '" + customPath + "'")

        for item in os.listdir(customPath):
            installationDir = customPath + "/" + item
            handler = self.action.createHandler(installationDir, "core")

            self.action.registerHandler(handler)
    
    # creates the applications equipment object
    def _createEquipment(self):

        setFile = self.appConfig.get("paths")["equipmentSet"]

        return Equipment(EquipmentSet(setFile))

    # shutdown the application and kill the process
    def stop(self):
        self.equipment.deloadEquipment()

        os.kill(os.getpid(), signal.SIGKILL)

    # reloads the application
    def reload(self):
        pass

    # returns the status observer
    def getStatusObserver(self):
        return self.statusObserver

    # returns the equipment
    def Equipment(self):
        return self.equipment

    # returns the action object
    def Action(self):
        return self.action

    # returns the main logger
    def getLogger(self):
        return self.logger

    # returns True if the application is in debug mode
    def isDebugMode(self):
        return self.systemConfig.get("config")["debug"] == True

    # returns the application config
    def getAppConfig(self):
        return self.appConfig

    # returns the system configuration
    def getSystemConfig(self):
        return self.systemConfig