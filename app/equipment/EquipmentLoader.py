from abc import ABC
from abc import abstractmethod
from lib.app.core.application.Application import Application

class EquipmentLoader(ABC):

    def __init__(self, equipmentGroupName, customLoadPath = None):

        self.logger = Application.app().getLogger()

        self.defaultLoadPath = "lib/defaults/" + equipmentGroupName

        if customLoadPath:
            self.customLoadPath = customLoadPath + equipmentGroupName
        else:
            self.customLoadPath = None
    
    def loadDefaultComponents(self):
        pass

    def loadCustomComponents(self):
        pass
        
    