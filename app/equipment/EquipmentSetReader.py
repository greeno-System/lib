from lib.app.core.config.ConfigReader import ConfigReader
import os.path
import xml.etree.ElementTree as ET

class EquipmentSetReader(ConfigReader):

    def load(self, root):

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

        return root.find("customLoadPath").text.strip().strip("/") + "/"

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

                config = self._getConfig(component)

                componentItem = {}
                componentItem["name"] = componentName
                
                if config is not False:
                    componentItem["config"] = config

                groups[groupName].append(componentItem)

        return groups

    def _getConfig(self, component):

        configElem = component.find("config")

        if configElem is None:
            return False

        configs = list(configElem)
        config = {}

        for item in configs:
            configName = item.tag
            value = item.text.strip()
            config[configName] = value

        return config


