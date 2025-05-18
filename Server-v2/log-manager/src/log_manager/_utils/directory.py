import os

class Directory:
    @staticmethod
    def ensure_dir_for_file(path: str) -> None:
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
