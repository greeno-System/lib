from lib.app.core.config.ConfigReader import ConfigReader

class AppConfigReader(ConfigReader):

    # creates the properties for application configuration
    def load(self, root):
        
        pathsElement = root.find("paths")

        paths = super().load(pathsElement)

        return {
            'paths': paths
        }