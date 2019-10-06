
class EquipmentManager():

    def __init__(self, equipmentCollection):

        if not equipmentCollection:
            raise ValueError("Equipment collection should not be None.")

        self.collection = equipmentCollection

    def loadEquipment(self):
        groups = self.collection.getGroups()

        baseLoadPath = "lib/defaults"