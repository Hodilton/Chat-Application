import os
from logging.handlers import TimedRotatingFileHandler

class TimeRotatingHandler(TimedRotatingFileHandler):
    def __init__(self, path: str, when: str = 'midnight', interval: int = 1, backup_count: int = 7):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        super().__init__(
            filename=path,
            when=when,
            interval=interval,
            backupCount=backup_count,
            encoding="utf-8",
            utc=True
        )
