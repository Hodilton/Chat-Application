from abc import ABC, abstractmethod

class FileHandler(ABC):
    @abstractmethod
    def write(self, file_path, data, overwrite=False):
        pass

    @abstractmethod
    def read(self, file_path):
        pass
