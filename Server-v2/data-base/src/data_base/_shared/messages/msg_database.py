from .msg_base import MsgBase

class MsgDataBase(MsgBase):
    class Success:
        @classmethod
        def connection_established(cls) -> None:
            MsgDataBase._logger.info("Database connection established successfully")

    class Failure:
        @classmethod
        def connection_failed(cls, error: str) -> None:
            MsgDataBase._logger.error(f"Database connection failed: {error}")

        @classmethod
        def query_failed(cls, query: str, error: str) -> None:
            MsgDataBase._logger.error(f"Query failed: {query} | Error: {error}")
