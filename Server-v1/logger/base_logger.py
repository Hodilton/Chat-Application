from abc import ABC, abstractmethod
from datetime import datetime

class Logger(ABC):
    @abstractmethod
    def log(self, message: str):
        pass

    def format_message(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] {message}"
