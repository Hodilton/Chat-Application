from file_work.src.file_processor import FileProcessor
from ..utils.utilities import Messages

class QueriesConfigLoader:
    def __init__(self, config_folder: str):
        self.config_folder = config_folder

    def load_config(self, table_name):
        config_path = {
            'folder_path': f"{self.config_folder}/queries",
            'file_name': table_name,
            'extension': 'json'
        }

        try:
            table_config = FileProcessor.read_file(config_path)
            Messages.Complete.table_load_queries(table_name)
            return table_config
        except Exception as e:
            Messages.Error.try_action(e)
            Messages.Error.table_load_queries(table_name)
            return None
