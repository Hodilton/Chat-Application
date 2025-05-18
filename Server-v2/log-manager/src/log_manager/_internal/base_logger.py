import logging

class LogFormatter:
    DEFAULT_FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
    DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def get_formatter():
        return logging.Formatter(LogFormatter.DEFAULT_FORMAT, LogFormatter.DEFAULT_DATE_FORMAT)
