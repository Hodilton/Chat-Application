from data_base._config.config_bootstrapper import ConfigBootstrapper
from .._infrastructure.aiomysql.aiomysql_connection import AioMySQLConnection
from .._infrastructure.database_wrapper import DatabaseWrapper

class DatabaseBuilder:
    def __init__(self, config_path: str):
        self._config_path = config_path

    async def build(self) -> DatabaseWrapper:
        bootstrapper = ConfigBootstrapper(self._config_path)
        if not bootstrapper.bootstrap():
            raise RuntimeError("Bootstrap failed")

        connection = AioMySQLConnection(bootstrapper.get_database_config())
        if not await connection.connect():
            raise RuntimeError("Database connection failed")

        return DatabaseWrapper(
            connection=connection,
            queries_dict=bootstrapper.get_queries_dict()
        )