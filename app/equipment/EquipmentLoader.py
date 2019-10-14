from abc import ABC
from abc import abstractmethod

class EquipmentLoader(ABC):

    def __init__(self, equipmentGroupName, customBasePath = None):
        self.defaultLoadPath = "lib/defaults/" + equipmentGroupName

        if customBasePath:
            self.customLoadPath = customBasePath.strip("/") + "/" + equipmentGroupName
        else:
            self.customLoadPath = None

    
    def loadDefaultComponents(self, componentDirectories):
        pass

    def loadCustomComponents(self):
        pass
        
    