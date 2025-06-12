from typing import Any, Tuple
import aiomysql

class AioMySQLRepository:
    def __init__(self, pool, queries: dict):
        self._pool = pool
        self._queries = queries

    async def execute(self, query: str, params: Tuple = ()) -> int:
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)
                return cur.rowcount

    async def fetch(self, query: str, params: Tuple = (), fetch_mode="one") -> Any:
        async with self._pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, params)
                if fetch_mode == "one":
                    return await cur.fetchone()
                return await cur.fetchall()