from file_work.src.file_processor import FileProcessor
from file_work.utils.utilities import Messages
from logger.log_manager import LogManager

def main():
    log_config = {
        "file_work": "logs/file.log",
    }

    LogManager.init_loggers(log_config)
    Messages.set_logger(LogManager.get_logger("file_work"))
    LogManager.log_program_start_for_all()

    config_path = {
        'folder_path': "./data",
        'file_name': 'tables_config',
        'extension': 'json'
    }

    data = {
        "2": "1"
    }

    FileProcessor.write_file(config_path, data, True)

    LogManager.log_program_end_for_all()

if __name__ == "__main__":
    main()
