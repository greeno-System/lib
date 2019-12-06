from abc import ABC
from abc import abstractmethod

class DataInterface(ABC):

    def __init__(self, config = False):

        self.config = config   

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass