from file_work.src.file_processor import FileProcessor
from ..utils.utilities import Messages

class TablesConfigLoader:
    def __init__(self, config_folder: str):
        self.config_folder = config_folder
        self.tables_config = None

    def load_config(self) -> bool:
        config_path = {
            'folder_path': self.config_folder,
            'file_name': 'tables_config',
            'extension': 'json'
        }

        try:
            config = FileProcessor.read_file(config_path)
            self.tables_config = config.get('tables', {})
            Messages.Complete.table_load_config()
            return True
        except Exception as e:
            Messages.Error.try_action(e)
            Messages.Error.table_load_config()
            return False
