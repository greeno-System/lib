from abc import ABC
from abc import abstractmethod

class DataInterface(ABC):

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass