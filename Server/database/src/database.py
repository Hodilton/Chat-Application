from ..config.db_loader import DBConfigLoader
from ..config.queries_loader import QueriesConfigLoader
from ..config.tables_loader import TablesConfigLoader
from ..connection.db_connection import DBConnection
from ..services.db_handler import DBHandler
from ..core.table import TablesContainer

'''
    # Добавляем автора по ФИО
    db.tables.authors.insert(("Достоевский", "Михайлович", "Фёдор"))
    id = db.tables.authors.insert(("Толстой", "Николаевич", "Лев"))

    # Обновляем автора с id=1
    is_success = db.tables.authors.update(("Толстой", "Николаевич", "Лев"), (1,))

    # Удаляем автора с id=1
    db.tables.authors.delete((1,))

    # 1. Получить автора по ID
    author = db.tables.authors.fetch("by_id", "one", (1,))

    # 2. Получить всех авторов
    all_authors = db.tables.authors.fetch("all", "all")

    # 3. Найти ID автора по ФИО (первая запись, если не уникальны)
    author_id = db.tables.authors.fetch("id_by_full_name", "one", ("Толстой", "Николаевич", "Лев"))

    # 4. Найти авторов по ФИО
    authors = db.tables.authors.fetch("by_full_name", "all", ("Толстой", "Николаевич", "Лев"))

    # 5. Поиск по части имени (LIKE)
    authors = db.tables.authors.fetch("by_partial_name", "all", ("%Толст%", "%Никол%", "%Лев%"))

    # 6. Получить количество авторов
    count = db.tables.authors.fetch("count", "one")[0]
'''

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
        self._handler.drop_tables()
        self._handler.create_tables()

    def close(self) -> None:
        if self._connection:
            self._connection.close()
