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

    def getSchema(self, xmlFile):
        if not os.path.isfile(xmlFile):
            raise FileNotFoundError("File '" + path + "' does not exist!")

        tree = ET.parse(xmlFile)
        root = tree.getroot()

        schemaLocation = root.get("{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation")

        if not schemaLocation:
            return None
        
        schema = xmlschema.XMLSchema(schemaLocation)

        return schema

    def isSchemaValid(self, path):
        if not os.path.isfile(path):
            raise FileNotFoundError("File '" + path + "' does not exist!")

        schema = self.getSchema(path)

        if schema:
            return schema.is_valid(path)
        
        return True

    def validateSchema(self, xmlFile, schema = None):

        if not xmlFile:
            raise ValueError("xml file path should not be None.")

        if not schema:
            schema = self.getSchema(xmlFile)
            
            if not schema:
                return

        schema.validate(xmlFile)