import aiomysql

class AioMySQLConnection:
    def __init__(self, config: dict):
        self._config = config
        self._pool = None

    async def connect(self) -> bool:
        try:
            self._pool = await aiomysql.create_pool(
                host=self._config["host"],
                user=self._config["user"],
                password=self._config["password"],
                db=self._config["name"],
                autocommit=True
            )
            return True
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            return False

    @property
    def is_connected(self) -> bool:
        return self._pool is not None

    async def close(self):
        if self._pool:
            self._pool.close()
            await self._pool.wait_closed()