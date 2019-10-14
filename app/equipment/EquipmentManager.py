import os.path
class EquipmentManager():

    def __init__(self, equipmentCollection):

        if not equipmentCollection:
            raise ValueError("Equipment collection should not be None.")

        self.collection = equipmentCollection

    def loadEquipment(self):
        groups = self.collection.getGroups()

        baseLoadPath = "lib/defaults"

        for groupName in groups:
            libPath = baseLoadPath + "/" + groupName

            print("loading equipment group '" + groupName + "' in '" + libPath + "'")

            if os.path.isdir(libPath):
                print("directory does exist!")
            else:
                print("directory not found!")

    