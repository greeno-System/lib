import os.path
from lib.app.equipment.EquipmentSetReader import EquipmentSetReader
from lib.app.core.config.Config import Config

class EquipmentSet():

    BASE_CORE_PATH = "lib/app/equipment/"
    DEFAULT_LOAD_PATH = "lib/defaults/equipment/"

    def __init__(self, equipmentFile):
        if not equipmentFile:
            raise ValueError("No equipment file given!")

        if not os.path.isfile(equipmentFile):
            raise FileNotFoundError("Equipment file '" + equipmentFile + "' does not exist!")

        self.config = self._createConfig(equipmentFile)

    
    def _createConfig(self, filePath):
        reader = EquipmentSetReader()

        return Config(filePath, reader)

    def getGroups(self):
        return self.config.get("groups")

    def getGroup(self, groupName):

        return self.config.get("groups")[groupName]

    def groupExists(self, groupName):

        if groupName is None:
            return False

        return os.path.isdir(EquipmentSet.BASE_CORE_PATH + groupName)

    def has(self, groupName, name):

        group = self.getGroup(groupName)

        if not group:
            return False

        return name in group

    def getCustomLoadPath(self):
        return self.config.get("customLoadPath")

    def hasCustomLoadPath(self):
        return self.config.get("customLoadPath") is not None