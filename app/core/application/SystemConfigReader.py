from lib.app.core.config.ConfigReader import ConfigReader
import os, os.path
import xml.etree.ElementTree as ET
import xmlschema

class SystemConfigReader(ConfigReader):

    # loads the system information with its configs
    def load(self, rootElement):

        properties = super().load(rootElement)

        configElement = rootElement.find("config")
        configs = super().load(configElement)

        configs["debug"] = bool(configs["debug"])

        properties["config"] = configs

        return properties