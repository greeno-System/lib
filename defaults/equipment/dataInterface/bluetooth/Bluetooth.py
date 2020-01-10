from lib.app.equipment.dataInterface.DataInterface import DataInterface
from lib.app.core.application.Application import Application
import _thread
import json

class Bluetooth(DataInterface):
    
    def __init__(self, config = False):

        super().__init__(config)

        self.logger = Application.app().getLogger()
        self.connection = Application.app().Equipment().get("connection", "bluetooth")
        self.action = Application.app().Action()

    def open(self):
        self.channel = self.connection.createChannel()
        self.channel.listen(1)

        self.connection.advertise(
            self.channel,
            self.config.get("serviceName"),
            self.config.get("uuid")
        )

        self.clientSocket = None
        self.remoteAddress = None

        self.isClosed = False

        self._waitForIncomingConnection()

    def _waitForIncomingConnection(self):
        self.clientSocket = None
        self.remoteAddress = None

        self.logger.debug("Bluetooth data interface waiting for incoming connection.")

        _thread.start_new_thread(self._acceptSocket, ())
        

    def _acceptSocket(self):
        self.clientSocket, self.remoteAddress = self.channel.accept()

        self.logger.debug(("Incoming bluetooth connection from ", self.remoteAddress))
        _thread.start_new_thread(self._listenForRequests, ())


    def _listenForRequests(self):
        self.logger.debug("Bluetooth listening for requests.")
        try:
            while True:
                data = self.connection.read(self.clientSocket)
                requestString = str(data, "UTF-8")

                jsonData = json.loads(requestString)

                print(jsonData)

                jsonResponse = self.action.request(jsonData)
                response = json.dumps(jsonResponse)

                self.connection.write(self.clientSocket, response)

        except Exception as e:
            if not self.isClosed:
                self._waitForIncomingConnection()

    def close(self):
        self.logger.debug("closing bluetooth dataInterface")

        self.isClosed = True

        if self.clientSocket is not None:
            self.clientSocket.close()