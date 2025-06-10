from ..config.db_loader import DBConfigLoader
from ..config.queries_loader import QueriesConfigLoader
from ..config.tables_loader import TablesConfigLoader
from ..connection.db_connection import DBConnection
from ..services.db_handler import DBHandler
from ..core.table import TablesContainer

class Database:
    def __init__(self, config_path: str):
        self._db_config_loader = DBConfigLoader(config_path)
        self._tables_config_loader = TablesConfigLoader(config_path)
        self._queries_loader = QueriesConfigLoader(config_path)

        self._connection = None
        self._handler = None
        self.tables = TablesContainer({})

    def connect(self) -> bool:
        if not self._db_config_loader.load_config():
            return False

        self._connection = DBConnection(
            config=self._db_config_loader.db_config
        )

        if not self._connection.connect():
            return False

        if not self._tables_config_loader.load_config():
            return False

        self._handler = DBHandler(
            connection=self._connection,
            queries_loader=self._queries_loader,
            tables_config=self._tables_config_loader.tables_config
        )

        self._handler.init_tables()
        self.tables = TablesContainer(self._handler.tables)
        return True

    def reset(self) -> None:
        if self._connection.is_connected:
            self._handler.drop_tables()
            self._handler.create_tables()

    def close(self) -> None:
        if self._connection:
            self._connection.close()
