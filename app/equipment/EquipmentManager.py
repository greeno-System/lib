import os.path
import logging
import importlib
from lib.app.equipment.EquipmentSet import EquipmentSet
class EquipmentManager():

    def __init__(self, equipmentSet):

        if not equipmentSet:
            raise ValueError("Equipment set should not be None.")

        self.set = equipmentSet

        from lib.app.core.application.Application import Application
        self.app = Application.app()

    def loadEquipment(self):
        groups = self.set.getGroups()

        customLoadPath = self.set.getCustomLoadPath()

        for groupName in groups:

            if not self.set.groupExists(groupName):
                self.app.getLogger().warning("Equipment group with name '" + groupName + "' does not exist!")
                continue
                
            installationPath = EquipmentSet.BASE_CORE_PATH + groupName

            groupLoader = self._createGroupLoader(installationPath, groupName, customLoadPath)

            if not groupLoader:
                continue

            defaultComponents = self.set.getGroup(groupName)
            groupLoader.loadDefaultComponents(defaultComponents)

    def _createGroupLoader(self, installationPath, groupName, customLoadPath=None):

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

            loader = loaderClass(groupName, customLoadPath)

        except Exception as e:
            self.app.getLogger().error(e)

            return False

        return loader
        