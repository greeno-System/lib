from lib.app.equipment.dataInterface.DataInterface import DataInterface
from lib.app.core.application.Application import Application

class Bluetooth(DataInterface):
    
    def __init__(self):
        self.logger = Application.app().getLogger()
        self.connection = Application.app().getEquipment().get("connection", "bluetooth")

    def open(self):
        self.logger.info("opening bluetooth dataInterface")

    def close(self):
        self.logger.info("closing bluetooth dataInterface")