import os.path
import logging
import importlib
from lib.app.equipment.EquipmentSet import EquipmentSet
class Equipment():

    def __init__(self, equipmentSet):

        if not equipmentSet:
            raise ValueError("Equipment set should not be None.")

        self.set = equipmentSet

        from lib.app.core.application.Application import Application
        self.app = Application.app()

        self.equipment = {}

    def getSet(self):
        return self.set

    def loadEquipment(self):
        defaults = self.set.getDefaultSequence()

        # customLoadPath = self.set.getCustomLoadPath()

        loaders = {}

        for componentItem in defaults:
            componentName = componentItem["name"]
            groupName = componentItem["group"]

            installationPath = EquipmentSet.BASE_CORE_PATH + groupName

            if not groupName in loaders:
                loader = self._createGroupLoader(installationPath, groupName)
                
                loaders[groupName] = loader
                self.equipment[groupName] = {}

            loader = loaders[groupName]

            componentInstallation = EquipmentSet.DEFAULT_LOAD_PATH + groupName + "/" + componentName + "/"
            component = loader.createComponent(componentInstallation)

            
            self.equipment[groupName][componentName] = component

        for componentItem in self.set.getDefaultSequence():
            componentName = componentItem["name"]
            groupName = componentItem["group"]
            
            loader = loaders[groupName]
            component = self.equipment[groupName][componentName]

            loader.loadComponent(component)

    def _createGroupLoader(self, installationPath, groupName):

        if installationPath is None:
            raise ValueError("Value of group loader installation path is not given.")

        if not os.path.isdir(installationPath):
            raise ValueError("installation path '" + installationPath + "' does not exist!")

        if groupName is None:
            raise ValueError("Group name is not given.")
                
        installationPath = installationPath.strip("/")
        loaderClass = groupName[0].capitalize() + groupName[1:len(groupName)] + "Loader"

        package = (installationPath + "/" + "Loader").replace("/", ".")
        loaderClass = getattr(importlib.import_module(package), loaderClass)

        loader = loaderClass(groupName)

        return loader

    def deloadEquipment(self):
        
        loadingSequence = reversed(self.set.getDefaultSequence())

        loaders = {}

        for item in loadingSequence:
            componentName = item["name"]
            groupName = item["group"]

            if groupName not in loaders:

                loader = self._createGroupLoader(
                    EquipmentSet.BASE_CORE_PATH + groupName,
                    groupName
                )

                loaders[groupName] = loader

            loader = loaders[groupName]

            component = self.get(groupName, componentName)
            loader.deloadComponent(component)

        del self.equipment
        self.equipment = {}

    def get(self, groupName, componentName):
        if not groupName in self.equipment:
            return None

        if not componentName in self.equipment[groupName]:
            return None

        return self.equipment[groupName][componentName]
        