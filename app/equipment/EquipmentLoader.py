from abc import ABC
from abc import abstractmethod
from lib.app.core.application.Application import Application
from lib.app.equipment.EquipmentSet import EquipmentSet
import os.path

class EquipmentLoader(ABC):

    def __init__(self, equipmentGroupName):

        self.logger = Application.app().getLogger()
        self.equipmentGroupName = equipmentGroupName
        
    @abstractmethod
    def loadComponent(self, installationPath):
        pass

    @abstractmethod
    def deloadComponent(self, component):
        pass

        
    