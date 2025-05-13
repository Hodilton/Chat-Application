from ..utils.utilities import Messages

from typing import Any, Optional, Dict

class Table:
    def __init__(self, table_manager):
        self._manager = table_manager

    @property
    def name(self) -> str:
        return self._manager.table_name

    def insert(self, data: tuple) -> Optional[int]:
        return self._manager.insert_data(data)

    def update(self, data: tuple, condition: tuple) -> bool:
        return self._manager.update_data(data, condition)

    def delete(self, query_name: str, condition: tuple) -> bool:
        return self._manager.delete_data(query_name, condition)

    def fetch(self, query_name: str,
                    fetch_mode: str = "one",
                    condition: tuple = ()
    ) -> Any:
        return self._manager.fetch(query_name, fetch_mode, condition)


class TablesContainer:
    def __init__(self, tables: Dict[str, Any]):
        self._tables = tables

    def __getattr__(self, name) -> Table:
        if name in self._tables:
            return Table(self._tables[name])
        raise Messages.Error.table_found(name)

    def __getitem__(self, name) -> Table:
        return self.__getattr__(name)