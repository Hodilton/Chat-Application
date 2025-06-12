from typing import Dict
from .base_aiorepository import BaseAioRepository
from .aiomysql.aiomysql_connection import AioMySQLConnection

class DatabaseWrapper:
    def __init__(self, connection: AioMySQLConnection, queries_dict: Dict[str, dict]) -> None:
        self._connection = connection
        self._queries_dict = queries_dict
        self._repositories: Dict[str, BaseAioRepository] = {}

    def get_repository(self, table_name: str) -> BaseAioRepository:
        if table_name not in self._repositories:
            queries = self._queries_dict.get(table_name)
            if not queries:
                raise ValueError(f"No queries found for table '{table_name}'")
            self._repositories[table_name] = BaseAioRepository(
                pool=self._connection.pool,
                queries=queries,
                table_name=table_name,
            )
        return self._repositories[table_name]

    @property
    def is_connected(self) -> bool:
        return self._connection.is_connected()

    async def close(self):
        await self._connection.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()