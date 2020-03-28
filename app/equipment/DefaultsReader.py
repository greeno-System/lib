from lib.app.core.config.ConfigReader import ConfigReader
import os.path
import xml.etree.ElementTree as ET

class DefaultsReader(ConfigReader):

    def load(self, root):

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

       
