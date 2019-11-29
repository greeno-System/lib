from lib.app.core.config.ConfigReader import ConfigReader
import os.path
import xml.etree.ElementTree as ET

class DefaultsReader(ConfigReader):

    def load(self, filePath):

        if not os.path.isfile(filePath):
            raise FileNotFoundError("File '" + filePath + "' does not exist!")

        if not self.isSchemaValid(filePath):
            raise ValueError("File '" + filePath + "' is not valid to it's schema!")

        tree = ET.parse(filePath)
        root = tree.getroot()

        return self._getDefaults(root)

    def _getDefaults(self, root):

        if root is None:
            return None

        componentList = list()
        components = list(root.findall("component"))

        for component in components:
            componentName = component.attrib["name"]
            componentGroup = component.attrib["group"]

            componentList.append({
                "name": componentName,
                "group": componentGroup
            })

        
        return componentList
