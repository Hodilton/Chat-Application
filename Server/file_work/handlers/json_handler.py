import json

from .file_handler import FileHandler
from ..utils.utilities import Messages

class JsonHandler(FileHandler):
    def write(self, file_path, data, overwrite=False):
        try:
            with open(file_path, 'w' if overwrite else 'x') as file:
                json.dump(data, file)
        except Exception as e:
            Messages.Error.try_action(e)
            return False
        return True

    def read(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            Messages.Error.try_action(e)
            return None
