import os
import os.path
import xml.etree.ElementTree as ET
import xmlschema

class ConfigReader():
    
    def load(self, path):

        if not os.path.isfile(path):
            raise FileNotFoundError("File '" + path + "' does not exist!")

        if not self.isSchemaValid(path):
            raise ValueError("XML file '" + path + "' is not valid to it's schema!")

        tree = ET.parse(path)
        root = tree.getroot()

        elements = list(root)
        properties = {}

        for elem in elements:
            tag = elem.tag
            value = elem.text.strip()
            properties[tag] = value 


        return properties

    def isSchemaValid(self, path):
        if not os.path.isfile(path):
            raise FileNotFoundError("File '" + path + "' does not exist!")

        tree = ET.parse(path)
        root = tree.getroot()

        schemaLocation = root.get("{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation")

        if schemaLocation:

            if not os.path.isfile(schemaLocation):
                return False

            schema = xmlschema.XMLSchema(schemaLocation)
            
            return schema.is_valid(path)
        
        return True