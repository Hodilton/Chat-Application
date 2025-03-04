import pandas as pd

from .file_handler import FileHandler
from ..utils.utilities import Messages

class CsvHandler(FileHandler):
    def write(self, file_path, data, overwrite=False):
        try:
            data_frame = pd.DataFrame(data)
            data_frame.to_csv(file_path, index=False, mode='w' if overwrite else 'x')
        except Exception as e:
            Messages.Error.try_action(e)
            return False
        return True

    def read(self, file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            Messages.Error.try_action(e)
            return None
