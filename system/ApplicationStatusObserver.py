from threading import Thread
from lib.system.SystemStatus import SystemStatus
import os, os.path
import sys

class ApplicationStatusObserver(Thread):

    def __init__(self, application, statusFile):
        Thread.__init__(self)
        self.app = application
        self.status = SystemStatus.APPLICATION_RUNNING
        self.statusFile = statusFile

        self.isRunning = False
        self.stop = False

    def run(self):

        self.isRunning = True
        self.stop = False

        while self.status == SystemStatus.APPLICATION_RUNNING and not self.stop:
            self.status = self.getStatusFromFile()

        self.isRunning = False

        if self.stop:
            return

        if self.status == SystemStatus.APPLICATION_RELOAD:
            self.app.reload()
            return
        
        self.app.stop()

    def getStatusFromFile(self):

        if os.path.isfile(self.statusFile):
            file = open(self.statusFile, 'r')
            newStatus = file.readline()
            file.close()

            return newStatus.strip().upper()

        raise FileNotFoundError("Application Status file was not found at '" + self.statusFile + "' ")

    def isRunning(self):
        return self.isRunning

    def stop(self):
        if self.isRunning:
            self.stop = True