from file_work.src.file_processor import FileProcessor
from ..utils.utilities import Messages

class DBConfigLoader:
    def __init__(self, config_folder: str):
        self.config_folder = config_folder
        self.db_config = None

    def load_config(self) -> bool:
        config_path = {
            'folder_path': self.config_folder,
            'file_name': 'db_config',
            'extension': 'json'
        }

        try:
            config = FileProcessor.read_file(config_path)
            self.db_config = config.get('database', {})
            Messages.Complete.db_load_config()
            return True
        except Exception as e:
            Messages.Error.try_action(e)
            Messages.Error.db_load_config()
            return False
