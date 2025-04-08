from ..utils.utilities import Messages

from typing import Any, Optional

class TableManager:
    def __init__(self, connection, table_name: str, queries: dict):
        self.table_name = table_name
        self.queries = queries
        self.connection = connection

    def create_table(self) -> bool:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(self.queries['create'])
                self.connection.commit()
            Messages.Complete.table_creating(self.table_name)
            return True
        except Exception as e:
            Messages.Error.try_action(e)
            Messages.Error.table_creating(self.table_name)
            return False

    def drop_table(self) -> bool:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(self.queries['drop'])
                self.connection.commit()
            Messages.Complete.table_droping(self.table_name)
            return True
        except Exception as e:
            Messages.Error.try_action(e)
            Messages.Error.table_droping(self.table_name)
            return False

    def insert_data(self, data: tuple) -> Optional[int]:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(self.queries['insert'], data)
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            Messages.Error.try_action(e)
            Messages.Error.data_inserting(self.table_name)
            return None

    def update_data(self, data: tuple, condition: tuple) -> bool:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(self.queries['update'], (*data, *condition))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            Messages.Error.try_action(e)
            Messages.Error.data_updating(self.table_name)
            return False

    def delete_data(self, condition: tuple) -> bool:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(self.queries['delete'], condition)
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            Messages.Error.try_action(e)
            Messages.Error.data_deleting(self.table_name)
            return False

    def fetch(self, query_name: str, fetch_mode: str, condition: tuple = ()) -> Any:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(self.queries['fetch'][query_name], condition)
                if fetch_mode == 'one':
                    result = cursor.fetchone()
                    if cursor.fetchone() is not None:
                        pass
                    return result
                elif fetch_mode == 'all':
                    return cursor.fetchall()
        except Exception as e:
            Messages.Error.try_action(e)
            Messages.Error.data_fetching(self.table_name)
            return None if fetch_mode == 'one' else []
