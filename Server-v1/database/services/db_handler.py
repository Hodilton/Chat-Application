from ..config.queries_loader import QueriesConfigLoader
from .table_manager import TableManager
from ..utils.utilities import Messages

class DBHandler:
    def __init__(self, connection,
                       queries_loader: QueriesConfigLoader,
                       tables_config: dict):
        self._queries_loader = queries_loader
        self._tables_config = tables_config
        self._connection = connection
        self.tables = {}

    def init_tables(self):
        for table_name, table_info in self._tables_config.items():
            try:
                queries = self._queries_loader.load_config(table_name)
                self.tables[table_name] = TableManager(
                    connection=self._connection.connection,
                    table_name=table_name,
                    queries=queries
                )

                Messages.Complete.table_initialized(table_name)
            except Exception as e:
                Messages.Error.try_action(e)
                Messages.Error.table_initialized(table_name)

    def create_tables(self):
        for table_name, table_info in self._tables_config.items():
            if table_name in self.tables:
                try:
                    self.tables[table_name].create_table()
                except Exception as e:
                    Messages.Error.try_action(e)

    def drop_tables(self):
        for table_name, table_info in reversed(self._tables_config.items()):
            if table_name in self.tables:
                try:
                    self.tables[table_name].drop_table()
                except Exception as e:
                    Messages.Error.try_action(e)
