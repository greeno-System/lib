import os.path
from lib.app.equipment.EquipmentSetReader import EquipmentSetReader
from lib.app.equipment.DefaultsReader import DefaultsReader
from lib.app.core.config.Config import Config

class EquipmentSet():

    BASE_CORE_PATH = "lib/app/equipment/"
    DEFAULT_LOAD_PATH = "lib/defaults/equipment/"

    def __init__(self, equipmentFile):
        if not equipmentFile:
            raise ValueError("No equipment file given!")

        if not os.path.isfile(equipmentFile):
            raise FileNotFoundError("Equipment file '" + equipmentFile + "' does not exist!")

        definitionSequence = self._createDefinitionSequence()
        config = self._createConfig(equipmentFile)

        defaultDefinitionSet = self._createDefaultDefinitionSet(definitionSequence)

        self.defaultSet = self._createDefaultSet(config, defaultDefinitionSet)
        self.defaultSequence = self._createDefaultSequence(self.defaultSet, definitionSequence)

        del definitionSequence
        del defaultDefinitionSet
        del config

    def _createDefinitionSequence(self):

        defaultsFile = EquipmentSet.DEFAULT_LOAD_PATH + "equipment.xml"
        reader = DefaultsReader()

        config = Config(defaultsFile, reader)

        return config.getProperties()

    def _createConfig(self, filePath):
        reader = EquipmentSetReader()

        return Config(filePath, reader)

    def _createDefaultDefinitionSet(self, definitionSequence):

        defaultSet = {}

        for item in definitionSequence:
            componentName = item["name"]
            groupName = item["group"]

            if not groupName in defaultSet:
                defaultSet[groupName] = {}

            defaultSet[groupName][componentName] = True

        return defaultSet

    def _createDefaultSet(self, config, defaultDefinitionSet):

        defaultSet = {}

        groups = config.get("groups")

        for groupName,components in groups.items():

            if groupName not in defaultDefinitionSet:
                continue

            defaultSet[groupName] = {}

            for componentName in components:
                
                if componentName in defaultDefinitionSet[groupName]:
                    defaultSet[groupName][componentName] = True

        return defaultSet

    def _createDefaultSequence(self, defaultSet, definitionSequence):

        sequence = []

        for item in definitionSequence:
            component = item["name"]
            group = item["group"]

            if group in defaultSet:
                if component in defaultSet[group]:

                    sequence.append(item)

        return sequence

    def getDefaultSequence(self):
        return self.defaultSequence
            

    def getGroups(self):
        return self.config.get("groups")

    def getGroup(self, groupName):
        
        if groupName is None or not groupName:
            return False

        if groupName in self.defaultSet:
            return self.defaultSet[groupName]

        return False

    def groupExists(self, groupName):

        if groupName is None or not groupName:
            return False

        return groupName in self.defaultSet

    def has(self, groupName, name):

        group = self.getGroup(groupName)

        if not group:
            return False

        return name in group

    # def getCustomLoadPath(self):
    #     return self.config.get("customLoadPath")

    # def hasCustomLoadPath(self):
    #     return self.config.get("customLoadPath") is not None