from lib.equipment.connection.MultiChannelConnection import MultiChannelConnection
from lib.app.core.application.Application import Application
import bluetooth

class Bluetooth(MultiChannelConnection):
    
    def open(self):
        self.logger.debug("Opening bluetooth connection")

    
    def close(self):
        self.logger.debug("Closing bluetooth connection")

    
    def write(self, channel):
        pass

    
    def read(self, channel):
        pass

    def createChannel(self):
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        socket.bind(("", bluetooth.PORT_ANY))

        return socket

    def advertise(self, channel, serviceName, uuid):

        if not channel:
            raise ValueError("No channel given!")

        if not serviceName or not serviceName.strip():
            raise ValueError("No service name given!")

        if not uuid or not uuid.strip():
            raise ValueError("No service UUID given!")

        bluetooth.advertise_service(
            channel,
            serviceName
            service_id=uuid,
            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
            profiles=[bluetooth.SERIAL_PORT_PROFILE]
        )

