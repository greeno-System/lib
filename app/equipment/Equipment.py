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
        return self.equipmentSet

    def loadEquipment(self):
        groups = self.set.getGroups()

        customLoadPath = self.set.getCustomLoadPath()

        for groupName in groups:

            if not self.set.groupExists(groupName):
                self.app.getLogger().warning("Equipment group with name '" + groupName + "' does not exist!")
                continue

            self.equipment[groupName] = {}

            installationPath = EquipmentSet.BASE_CORE_PATH + groupName

            groupLoader = self._createGroupLoader(installationPath, groupName)

            if not groupLoader:
                continue

            defaultComponents = self.set.getGroup(groupName)

            for componentName in defaultComponents:
                installationPath = EquipmentSet.DEFAULT_LOAD_PATH + groupName + "/" + componentName + "/"

                component = groupLoader.loadComponent(installationPath)

                if component is not None and component is not False:
                    self.equipment[groupName][componentName] = component

    def _createGroupLoader(self, installationPath, groupName):

        if installationPath is None:
            raise ValueError("Value of group loader installation path is not given.")

        if not os.path.isdir(installationPath):
            raise ValueError("installation path '" + installationPath + "' does not exist!")

        if groupName is None:
            raise ValueError("Group name is not given.")

        try:
                
            installationPath = installationPath.strip("/")
            loaderClass = groupName.capitalize() + "Loader"

            package = (installationPath + "/" + "Loader").replace("/", ".")
            loaderClass = getattr(importlib.import_module(package), loaderClass)

            loader = loaderClass(groupName)

        except Exception as e:
            self.app.getLogger().error(e)

            return False

        return loader

    def deloadEquipment(self):
        
        for groupName,components in self.equipment.items():

            installationPath = EquipmentSet.BASE_CORE_PATH + groupName
            loader = self._createGroupLoader(installationPath, groupName)

            for componentName,component in components.items():
                loader.deloadComponent(component)

        del self.equipment
        self.equipment = {}

    def get(self, groupName, componentName):
        if not groupName in self.equipment:
            return None

        if not componentName in self.equipment[groupName]:
            return None

        return self.equipment[groupName][componentName]
        