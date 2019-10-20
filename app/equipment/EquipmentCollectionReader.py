from lib.app.core.config.ConfigReader import ConfigReader
import os.path
import xml.etree.ElementTree as ET

class EquipmentCollectionReader(ConfigReader):

    def load(self, filePath):
        if not os.path.isfile(filePath):
            raise FileNotFoundError("File '" + filePath + "' does not exist!")

        if not self.isSchemaValid(filePath):
            raise ValueError("The equipment file is not valid to equipment schema!")

        tree = ET.parse(filePath)
        root = tree.getroot()

        properties = {}

        customLoadPath = self._getCustomLoadPath(root)

        if customLoadPath:
            properties["customLoadPath"] = customLoadPath
        
        
        defaults = self._getDefaults(root)

        if defaults != False:
            properties["groups"] = defaults

        return properties

    def _getCustomLoadPath(self, root):

        if root is None:
            return False

        if root.find("customLoadPath") is None:
            return False

        if root.find("customLoadPath").text.strip() == "":

            return False

        return root.find("customLoadPath").text.strip()

    def _getDefaults(self, root):

        if root is None:
            return False

        defaultsElem = root.find("defaults")

        if defaultsElem is None:
            return False

        groupElems = list(defaultsElem.findall("group"))

        if not groupElems or len(groupElems) == 0:
            return False

        groups = {}

        for group in groupElems:
            groupName = group.attrib["name"]

            groups[groupName] = []

            for component in list(group.findall("component")):
                componentName = component.attrib["name"]

                groups[groupName].append(componentName)

        return groups

