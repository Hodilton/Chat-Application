from file_work.utils.utilities import Messages as MessagesFile
from database.utils.utilities import Messages as MessagesDB
from logger.log_manager import LogManager

from database.src.database import Database
from flask_app.app import app, init_db

def main():
    log_config = {
        "file_work": "logs/file.log",
        "db_work": "logs/database.log",
    }

    LogManager.init_loggers(log_config)
    MessagesFile.set_logger(LogManager.get_logger("file_work"))
    MessagesDB.set_logger(LogManager.get_logger("db_work"))

    LogManager.clear_log_for_all()
    LogManager.log_program_start_for_all()

    db = Database("data")
    db.connect()
    # db.reset()

    init_db(db)
    app.run(host='0.0.0.0', port=8000)

    db.close()
    LogManager.log_program_end_for_all()

if __name__ == "__main__":
    main()
