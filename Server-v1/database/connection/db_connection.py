import mysql.connector
from mysql.connector import errorcode

from ..utils.utilities import Messages

class DBConnection:
    def __init__(self, config: dict):
        self.config = config
        self.connection = None

    def connect(self)-> bool:
        if self.is_connected:
            Messages.Error.connection_already_established(self.config.get('database'))
            return True

        try:
            self.connection = mysql.connector.connect(
                host=self.config.get('host'),
                user=self.config.get('user'),
                password=self.config.get('password'),
                database=self.config.get('name')
            )

            Messages.Complete.connection(self.config.get('name'))
            return True
        except mysql.connector.Error as e:
            self._handle_error(e)
            Messages.Error.connection(self.config.get('name'))
            return False

    @property
    def is_connected(self) -> bool:
        return self.connection is not None

    def close(self):
        if self.is_connected:
            try:
                self.connection.close()
                self.connection = None
                Messages.Complete.close_connection(self.config.get('name'))
            except Exception as e:
                Messages.Error.try_action(e)
        else:
            Messages.Error.miss_connection(self.config.get('name'))

    def _handle_error(self, error: errorcode):
        error_mapping = {
            1045: "Access denied: Check your username or password.",
            1049: "Database does not exist.",
            2003: "Cannot connect to database server."
        }
        Messages.Error.try_action(f"Database error [{error.errno}]: {error_mapping.get(error.errno, str(error))}")