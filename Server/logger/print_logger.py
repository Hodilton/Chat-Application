from .base_logger import Logger

class PrintLogger(Logger):
    def log(self, message: str):
        formatted_message = self.format_message(message)
        print(formatted_message)
