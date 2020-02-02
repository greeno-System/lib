import os
import os.path
import xml.etree.ElementTree as ET
import xmlschema

class ConfigReader():

    # parses the given xml file and returns the loaded properties
    # if the xml file contains a schema location the validity of the file to its schema will be checked
    # if the file is not valid to its schema a ValueError will be thrown
    def loadFromFile(self, path):

        if not os.path.isfile(path):
            raise FileNotFoundError("File '" + path + "' does not exist!")

        if not self.isSchemaValid(path):
            raise ValueError("XML file '" + path + "' is not valid to it's schema!")
        
        tree = ET.parse(path)
        rootElement = tree.getroot()

        return self.load(rootElement)

    
    # creates a dictionary from simple xml file with only leaves
    def load(self, root):

        if root is None or not root:
            raise ValueError("No XML root element given!")

        elements = list(root)
        properties = {}

        for elem in elements:
            tag = elem.tag
            value = elem.text.strip()
            properties[tag] = value 


        return properties

    # returns the schema object of a given xml file
    # returns None if the root element doesn't declare a schema location
    def getSchema(self, path):

        tree = ET.parse(path)
        root = tree.getroot()

        schemaLocation = root.get("{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation")

        if not schemaLocation:
            return None
        
        schema = xmlschema.XMLSchema(schemaLocation)

        return schema

    # returns True if the xml file is valid to it's schema or doesn't declare a schema location
    def isSchemaValid(self, path):

        schema = self.getSchema(path)

        if schema:
            return schema.is_valid(path)
        
        return True

    # validates an xml file to it's schema
    def validateSchema(self, xmlFile, schema = None):

        if not xmlFile:
            raise ValueError("xml file path should not be None.")

        if schema is None:
            schema = self.getSchema(xmlFile)
            
            if schema is None:
                return

        schema.validate(xmlFile)