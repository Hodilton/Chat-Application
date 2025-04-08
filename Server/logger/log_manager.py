import os

from logger.file_logger import FileLogger
from logger.print_logger import PrintLogger

class LogManager:
    LOG_DIR = "logs"
    _loggers = {}

    @classmethod
    def init_loggers(cls, log_config=None):
        os.makedirs(cls.LOG_DIR, exist_ok=True)

        log_config = log_config or {
            "main": os.path.join(cls.LOG_DIR, "main.log"),
        }

        for key, path in log_config.items():
            cls._loggers[key] = FileLogger(path)

    @classmethod
    def get_logger(cls, log_name):
        return cls._loggers.get(log_name, PrintLogger())

    @classmethod
    def log(cls, log_name, message):
        if log_name in cls._loggers:
            cls._loggers[log_name].log(message)
        else:
            print(f"❌ Log '{log_name}' not found.!")

    @classmethod
    def clear_log(cls, log_name):
        if log_name in cls._loggers:
            open(cls._loggers[log_name].file_path, 'w').close()

    @classmethod
    def clear_log_for_all(cls):
        for log_name in cls._loggers:
            cls.clear_log(log_name)

    @classmethod
    def log_program_start_for_all(cls):
        for log_name in cls._loggers:
            cls.log_program_start(log_name)

    @classmethod
    def log_program_end_for_all(cls):
        for log_name in cls._loggers:
            cls.log_program_end(log_name)

    @classmethod
    def log_program_start(cls, log_name):
        start_message = "🔸 Program start."
        cls.add_blank_line(log_name)
        cls.log(log_name, start_message)

    @classmethod
    def log_program_end(cls, log_name):
        end_message = "🔸 Program end."
        cls.log(log_name, end_message)
        cls.add_blank_line(log_name)

    @classmethod
    def add_blank_line(cls, log_name):
        cls.log(log_name, "")
