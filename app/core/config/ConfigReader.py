import os
import os.path
import xml.etree.ElementTree as ET
import xmlschema

class ConfigReader():
    
    def load(self, path):

        if not os.path.isfile(path):
            raise FileNotFoundError("File '" + path + "' does not exist!")

        self.validateSchema(path)

        tree = ET.parse(path)
        root = tree.getroot()

        elements = list(root)
        properties = {}

        for elem in elements:
            tag = elem.tag
            value = elem.text.strip()
            properties[tag] = value 


        return properties

    def validateSchema(self, path):
        if not os.path.isfile(path):
            raise FileNotFoundError("File '" + path + "' does not exist!")

        tree = ET.parse(path)
        root = tree.getroot()

        schemaLocation = root.get("{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation")

        if schemaLocation:

            if not os.path.isfile(schemaLocation):
                raise ValueError("XML schema was not found at '" + schemaLocation + "'")

            schema = xmlschema.XMLSchema(schemaLocation)
            schema.validate(path)