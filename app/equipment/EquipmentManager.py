import os.path
import logging
import importlib
from lib.app.equipment.EquipmentCollection import EquipmentCollection
class EquipmentManager():

    def __init__(self, equipmentCollection):

        if not equipmentCollection:
            raise ValueError("Equipment collection should not be None.")

        self.collection = equipmentCollection

        from lib.app.core.application.Application import Application
        self.app = Application.app()

    def loadEquipment(self):
        groups = self.collection.getGroups()

        customLoadPath = self.collection.getCustomLoadPath()

        for groupName in groups:

            if not self.collection.groupExists(groupName):
                self.app.getLogger().warning("Equipment group with name '" + groupName + "' does not exist!")
                continue
                
            installationPath = EquipmentCollection.BASE_CORE_PATH + groupName

            groupLoader = self._createGroupLoader(installationPath, groupName, customLoadPath)

            if not groupLoader:
                continue

            groupLoader.loadDefaultComponents()

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
        