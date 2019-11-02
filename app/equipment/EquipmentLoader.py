from abc import ABC
from abc import abstractmethod
from lib.app.core.application.Application import Application
from lib.app.equipment.EquipmentSet import EquipmentSet
import os.path

class EquipmentLoader(ABC):

    def __init__(self, equipmentGroupName, customLoadPath = None):

        self.logger = Application.app().getLogger()
        self.equipmentGroupName = equipmentGroupName

        self.defaultLoadPath = EquipmentSet.DEFAULT_LOAD_PATH + equipmentGroupName

        if customLoadPath:
            self.customLoadPath = customLoadPath + equipmentGroupName
        else:
            self.customLoadPath = None
    
    
    def loadDefaultComponents(self, defaultComponents):
        
        if defaultComponents is None:
            return False

        for componentName in defaultComponents:
            installationPath = EquipmentSet.DEFAULT_LOAD_PATH + self.equipmentGroupName + "/" + componentName

            if not os.path.isdir(installationPath):
                raise FileNotFoundError("the installation path '" + installationPath + "' for component '" + componentName + "' does not exist.")

            self.loadComponent(installationPath)
            

    
    def loadCustomComponents(self):
        pass

    @abstractmethod
    def isLoadable(self, installationPath):
        pass

    @abstractmethod
    def loadComponent(self, installationPath):
        pass

        
    