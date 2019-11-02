from lib.app.equipment.EquipmentLoader import EquipmentLoader

class ConnectionLoader(EquipmentLoader):

    def test(self):
        print("hello from connection loader!")

    def loadComponent(self, installationPath):
        pass

    def isLoadable(self):
        pass