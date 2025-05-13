import os

from .base_logger import Logger

class FileLogger(Logger):
    def __init__(self, file_path):
        self.file_path = file_path

        log_dir = os.path.dirname(file_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

    def log(self, message: str):
        formatted_message = self.format_message(message)
        try:
            with open(self.file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(formatted_message + '\n')
        except Exception as e:
            print(f"❌ Ошибка при записи лога: {e}")
