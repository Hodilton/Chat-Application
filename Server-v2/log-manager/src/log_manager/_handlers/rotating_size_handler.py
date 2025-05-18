import os
from logging.handlers import RotatingFileHandler

class RotatingSizeHandler(RotatingFileHandler):
    def __init__(self, path: str, max_bytes: int = 10240, backup_count: int = 3):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        super().__init__(
            filename=path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
