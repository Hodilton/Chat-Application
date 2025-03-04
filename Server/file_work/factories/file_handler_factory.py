from ..handlers.csv_handler import CsvHandler
from ..handlers.json_handler import JsonHandler
from ..handlers.binary_handler import BinaryHandler

from ..utils.utilities import Messages

class FileHandlerFactory:
    @staticmethod
    def create_handler(extension):
        if extension == 'csv':
            return CsvHandler()
        elif extension == 'json':
            return JsonHandler()
        elif extension == 'bin':
            return BinaryHandler()
        else:
            Messages.Error.file_format_not_supported(extension)
            return None
