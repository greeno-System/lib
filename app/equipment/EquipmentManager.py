import os.path
class EquipmentManager():

    def __init__(self, equipmentCollection):

        if not equipmentCollection:
            raise ValueError("Equipment collection should not be None.")

        self.collection = equipmentCollection

    def loadEquipment(self):
        groups = self.collection.getGroups()

        baseLoadPath = "lib/defaults"
        baseCorePath = "lib/equipment"

        print(groups)
        return


        for groupName in groups:

            if not self.groupExists(groupName):
                print("equipment group with name '" + groupName + "' is unknown")
                continue

            corePath = baseCorePath + "/" + groupName
            libPath = baseLoadPath + "/" + groupName

            print("loading equipment group '" + groupName + "' in '" + libPath + "'")

            if os.path.isdir(libPath):
                print("directory does exist!")
            else:
                print("directory not found!")

    def groupExists(self, groupName):
        
        if not groupName:
            return False

        corePath = "lib/equipment/" + groupName

        return os.path.isdir(corePath)