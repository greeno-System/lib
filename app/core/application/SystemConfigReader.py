from lib.app.core.config.ConfigReader import ConfigReader
import os, os.path
import xml.etree.ElementTree as ET
import xmlschema

class SystemConfigReader(ConfigReader):

    def load(self, filePath):
        if not os.path.isfile(filePath):
            raise FileNotFoundError("File '" + filePath + "' does not exist!")

        if not self.isSchemaValid(filePath):
            raise ValueError("The equipment file is not valid to equipment schema!")

        properties = super().load(filePath)

        tree = ET.parse(filePath)
        root = tree.getroot()

        configs = self._getConfigs(root)

        properties["config"] = configs

        return properties

    def _getConfigs(self, rootElement):
        configElem = rootElement.find("config")

        return {
            'debug': configElem.find("debug").text.strip() == 'true'
        }
