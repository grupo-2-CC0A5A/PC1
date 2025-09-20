import sqlite3 as sqlite
from pathlib import Path


class DB:
    def __init__(self, db_path, file):
        if isinstance(db_path, str):
            db_path = Path(db_path)
        self._db_path = db_path / f"{file}.db"
        self._db = sqlite.connect(self._db_path)
        if not self.table_exists():
            self.create_table()

    def create_table(self):
        cursor = self._db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                marca TEXT NOT NULL,
                talla INTEGER NOT NULL,
                precio REAL NOT NULL,
                numPares INTEGER NOT NULL
            )
        ''')
        self._db.commit()

    def create(self, item):
        cursor = self._db.cursor()
        cursor.execute(
            "INSERT INTO items (marca, talla, precio, numPares) VALUES (?, ?, ?, ?)",
            (item["marca"], item["talla"], item["precio"], item["numPares"]),
        )
        self._db.commit()
        return cursor.lastrowid

    def read(self, id):
        cursor = self._db.cursor()
        cursor.execute("SELECT * FROM items WHERE id = ?", (id,))
        item = cursor.fetchone()
        return item

    def read_all(self):
        cursor = self._db.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        return items

    def update(self, id, mods) -> None:
        changes = {k: v for k, v in mods.items() if v is not None}
        if not changes:
            return

        set_clause = ", ".join([f"{key} = ?" for key in changes.keys()])
        values = list(changes.values()) + [id]

        cursor = self._db.cursor()
        cursor.execute(
            f"UPDATE items SET {set_clause} WHERE id = ?",
            values
        )
        self._db.commit()

    def delete(self, id) -> None:
        cursor = self._db.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (id,))
        self._db.commit()

    def delete_all(self) -> None:
        cursor = self._db.cursor()
        cursor.execute("DELETE FROM items")
        self._db.commit()

    def count(self):
        cursor = self._db.cursor()
        cursor.execute("SELECT COUNT(*) FROM items")
        count = cursor.fetchone()[0]
        return count

    def close(self):
        self._db.close()

    def table_exists(self, table_name="items"):
        cursor = self._db.cursor()
        cursor.execute('''
            SELECT name FROM sqlite_master
            WHERE type='table' AND name=?
        ''', (table_name,))
        return cursor.fetchone() is not None

    def find_by_marca_talla(self, marca, talla):
        cursor = self._db.cursor()
        cursor.execute("SELECT * FROM items WHERE marca = ? AND talla = ?", (marca, talla))
        item = cursor.fetchone()
        return item