from lib.core.config.ConfigReader import ConfigReader
import os.path
import xml.etree.ElementTree as ET

class EquipmentCollectionReader(ConfigReader):

    def load(self, filePath):
        if not os.path.isfile(filePath):
            raise FileNotFoundError("File '" + filePath + "' does not exist!")

        tree = ET.parse(filePath)
        root = tree.getroot()

        elements = list(root)

        properties = {}

        for elem in elements:
            tag = elem.tag

            if not tag in properties:
                properties[tag] = []

            equipments = list(elem)

            for e in equipments:
                name = e.text.strip()
                properties[tag].append(name)

        return properties