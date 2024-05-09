# database.py


import sqlite3
from p2app.events import *


class DatabaseManager:
    def __init__(self):
        self._conn = None
        self.path = None

    def open_database(self, event):
        try:
            self.path = event.path()
            self._conn = sqlite3.connect(self.path)
            self._conn.execute("PRAGMA foreign_keys = ON;")
            yield DatabaseOpenedEvent(self.path)
        except sqlite3.Error as e:
            yield DatabaseOpenFailedEvent(str(e))

    def connection(self):
        return self._conn

    def database_path(self):
        return self.path
