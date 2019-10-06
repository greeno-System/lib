import os.path
from lib.app.equipment.EquipmentCollectionReader import EquipmentCollectionReader
from lib.app.core.config.Config import Config

class EquipmentCollection():

    def __init__(self, equipmentFile):
        if not equipmentFile:
            raise ValueError("No equipment file given!")

        if not os.path.isfile(equipmentFile):
            raise FileNotFoundError("Equipment file '" + equipmentFile + "' does not exist!")

        self.config = self._createConfig(equipmentFile)

    
    def _createConfig(self, filePath):
        reader = EquipmentCollectionReader()

        return Config(filePath, reader)

    def getGroups(self):
        return list(self.config.getProperties().keys())

    def getGroup(self, groupName):

        return self.config.get(groupName)

    def has(self, groupName, name):

        group = self.getGroup(groupName)

        if not group:
            return False

        return name in group