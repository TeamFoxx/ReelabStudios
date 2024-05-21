import sqlite3
import random
from contextlib import contextmanager
from typing import Optional, Dict, List, Union


class SQLiteCRUD:
    def __init__(
        self,
        db_path: str,
        table_name: str,
        columns: Dict[str, str],
    ):
        """
        Initialize SQLiteCRUD instance.

        :param db_path: Path to the SQLite database file.
        :param table_name: Name of the database table.
        :param columns: Dictionary containing column names and their data types.

        Example:

        >> db_path = "your_database.db"
        >> table_name = "your_table"
        >> columns = {"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "name": "TEXT", "age": "INTEGER"}
        >> crud_instance = SQLiteCRUD(db_path, table_name, columns)
        """
        self.db_path = db_path
        self.table_name = table_name
        self.columns = columns

    @contextmanager
    def _get_connection_cursor(self):
        """
        Context manager for obtaining a database connection cursor.

        :yield: Database cursor.
        """
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()
            connection.commit()
            connection.close()

    def create_table(self):
        """
        Create a table in the database.
        """
        columns_str = ", ".join(
            f"{column} {data_type}" for column, data_type in self.columns.items()
        )
        create_table_query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns_str})"
        with self._get_connection_cursor() as cursor:
            cursor.execute(create_table_query)

    def create(self, data: Dict[str, Union[str, int]]):
        """
        Insert a record into the database.
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data.values())
        insert_query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        with self._get_connection_cursor() as cursor:
            cursor.execute(insert_query, tuple(data.values()))

    def read_all(self):
        """
        Read all records from the database.
        """
        select_query = f"SELECT * FROM {self.table_name}"
        with self._get_connection_cursor() as cursor:
            cursor.execute(select_query)
            return cursor.fetchall()

    def read(self, conditions: Dict[str, Union[str, int]]):
        """
        Read a record from the database based on conditions.
        """
        where_conditions = " AND ".join(f"{key} = ?" for key in conditions.keys())
        select_query = f"SELECT * FROM {self.table_name} WHERE {where_conditions}"
        with self._get_connection_cursor() as cursor:
            cursor.execute(select_query, tuple(conditions.values()))
            return cursor.fetchone()

    def update(self, data: Dict[str, Union[str, int]], conditions: Dict[str, Union[str, int]]):
        """
        Update records in the database based on conditions.
        """
        set_clause = ", ".join(f"{key} = ?" for key in data.keys())
        where_conditions = " AND ".join(f"{key} = ?" for key in conditions.keys())
        update_query = f"UPDATE {self.table_name} SET {set_clause} WHERE {where_conditions}"
        with self._get_connection_cursor() as cursor:
            cursor.execute(update_query, tuple(data.values()) + tuple(conditions.values()))

    def delete(self, conditions: Dict[str, Union[str, int]]):
        """
        Delete records from the database based on conditions.
        """
        where_conditions = " AND ".join(f"{key} = ?" for key in conditions.keys())
        delete_query = f"DELETE FROM {self.table_name} WHERE {where_conditions}"
        with self._get_connection_cursor() as cursor:
            cursor.execute(delete_query, tuple(conditions.values()))

    def get_random_item(self):
        """
        Get a random record from the database.
        """
        count_query = f"SELECT COUNT(*) FROM {self.table_name}"
        with self._get_connection_cursor() as cursor:
            cursor.execute(count_query)
            total_rows = cursor.fetchone()[0]
            if total_rows > 0:
                random_offset = random.randint(0, total_rows - 1)
                select_query = f"SELECT * FROM {self.table_name} LIMIT 1 OFFSET {random_offset}"
                cursor.execute(select_query)
                return cursor.fetchone()
            else:
                return None

    def execute_query(
        self,
        query: str,
        params: Optional[tuple] = None,
        fetch_result: bool = False,
    ):
        """
        Execute a custom SQL query.
        """
        with self._get_connection_cursor() as cursor:
            cursor.execute(query, params or ())
            if fetch_result:
                return cursor.fetchall()
