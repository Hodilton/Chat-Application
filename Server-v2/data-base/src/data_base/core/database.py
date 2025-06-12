from .database_builder import DatabaseBuilder

class Database:
    _instance = None

    def __init__(self):
        self._db = None

    async def __aenter__(self):
        if Database._instance is None:
            builder = DatabaseBuilder("config/database")
            Database._instance = await builder.build()
        self._db = Database._instance
        return self._db

    async def __aexit__(self, exc_type, exc, tb):
        pass

    @classmethod
    async def close_instance(cls):
        if cls._instance is not None:
            await cls._instance.close()
            cls._instance = None