from .file_handler import FileHandler
from ..utils.utilities import Messages

class BinaryHandler(FileHandler):
    def write(self, file_path, data, overwrite=False):
        try:
            mode = 'wb' if overwrite else 'xb'
            with open(file_path, mode) as file:
                binary_data = data.encode('utf-8')
                file.write(binary_data)
        except Exception as e:
            Messages.Error.try_action(e)
            return False
        return True

    def read(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                binary_data = file.read()
                decoded_data = binary_data.decode('utf-8')
                return decoded_data
        except Exception as e:
            Messages.Error.try_action(e)
            return None
