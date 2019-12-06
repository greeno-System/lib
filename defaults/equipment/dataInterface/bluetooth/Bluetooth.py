from lib.app.equipment.dataInterface.DataInterface import DataInterface
from lib.app.core.application.Application import Application

class Bluetooth(DataInterface):
    
    def __init__(self, config = False):

        super().__init__(config)

        self.logger = Application.app().getLogger()
        self.connection = Application.app().Equipment().get("connection", "bluetooth")
        self.action = Application.app().Action()

    def open(self):
        self.socket = self.connection.createChannel()
        self.socket.listen(1)

    def close(self):
        self.logger.info("closing bluetooth dataInterface")