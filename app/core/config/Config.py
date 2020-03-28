import os.path
from lib.app.core.config.ConfigReader import ConfigReader
import xml.etree.ElementTree as ET
import xmlschema

class Config():

    # constructor
    # takes the relative or absolute path to the xml file,
    # an optional config reader and an optional 'extend' flag
    #
    # if reader is None a default reader will be used
    # the custom reader can extend the default reader with extend=True
    #
    # config will be loaded automatically
    def __init__(self, path, reader=None, extend=False):

        if path == None:
            raise ValueError("No file path given.")

        self.extendReader = None

        if reader == None:
            self.reader = ConfigReader()
        elif extend == False:
            self.reader = reader
        else:
            self.reader = ConfigReader()
            self.extendReader = reader


        self.path = path
        self.reload()

    # (re)loads the properties from reader(s)
    # existing properties will be overwritten
    def reload(self):

        self.properties = self.reader.loadFromFile(self.path)

        if self.extendReader != None:
            props = self.extendReader.loadFromFile(self.path)
            self.properties.update(props)

        self.loaded = True

    # returns the value of a property
    def get(self, propertyname):

        if propertyname in self.properties:
            return self.properties[propertyname]
            
        return None
            
    # returns all properties
    def getAll(self):
        return self.properties