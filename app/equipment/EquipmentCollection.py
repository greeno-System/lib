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

    def getCollection(self, collectionName):

        return self.config.get(collectionName)

    def has(self, collectionName, equipmentName):

        collection = self.getCollection(collectionName)

        if not collection:
            return False

        return equipmentName in collection