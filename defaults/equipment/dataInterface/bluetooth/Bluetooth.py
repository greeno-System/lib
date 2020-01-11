from lib.app.equipment.dataInterface.DataInterface import DataInterface
from lib.app.core.application.Application import Application
import _thread
import json

class Bluetooth(DataInterface):
    
    # constructor
    def __init__(self, config = False):

        super().__init__(config)

        self.logger = Application.app().getLogger()
        self.connection = Application.app().Equipment().get("connection", "bluetooth")

    # opens the bluetooth data interface and starts waiting for incoming connections
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

    # helper function to start a new thread which will be blocked until a new connection is incoming
    def _waitForIncomingConnection(self):
        self.clientSocket = None
        self.remoteAddress = None

        self.logger.debug("Bluetooth data interface waiting for incoming connection.")

        _thread.start_new_thread(self._acceptSocket, ())
        

    # helper function which will be blocked until a new socket is accepted.
    # Starts a new thread for getting requests after successful connection
    def _acceptSocket(self):
        self.clientSocket, self.remoteAddress = self.channel.accept()

        self.logger.debug(("Incoming bluetooth connection from ", self.remoteAddress))
        _thread.start_new_thread(self._listenForRequests, ())

    # infinite loop through all incoming requests from existing bluetooth connection
    # In case of broken connection waiting for new connection is starting
    def _listenForRequests(self):
        self.logger.debug("Bluetooth listening for requests.")
        try:
            while True:
                data = self.connection.read(self.clientSocket)
                requestString = str(data, "UTF-8")

                jsonData = json.loads(requestString)

                jsonResponse = self.request(jsonData)
                response = json.dumps(jsonResponse)

                self.connection.write(self.clientSocket, response)

        except Exception as e:
            if not self.isClosed:
                self._waitForIncomingConnection()

    # closes and disables the interface
    def close(self):
        self.logger.debug("closing bluetooth dataInterface")

        self.isClosed = True

        if self.clientSocket is not None:
            self.clientSocket.close()