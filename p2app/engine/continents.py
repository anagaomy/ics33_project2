# continents.py


import sqlite3
from p2app.events import *


class ContinentManager:
    def __init__(self, connection):
        self._conn = connection

    def start_continent_search(self, event):
        search_criteria = event.continent_code(), event.name()

        if event.continent_code() is None or event.name() is None:
            query = "SELECT * FROM continent WHERE continent_code = ? OR name = ?"
        else:
            query = "SELECT * FROM continent WHERE continent_code = ? AND name = ?"

        cursor = self._conn.cursor()
        cursor.execute(query, search_criteria)
        _continents = cursor.fetchall()
        cursor.close()
        for continent in _continents:
            yield ContinentSearchResultEvent(Continent(*continent))

    def load_continent(self, event):
        continent_id = event.continent_id()
        query = "SELECT * FROM continent WHERE continent_id = ?"
        cursor = self._conn.cursor()
        cursor.execute(query, (continent_id,))
        _continent = cursor.fetchone()
        cursor.close()
        if _continent:
            yield ContinentLoadedEvent(Continent(*_continent))

    def save_new_continent(self, event):
        _continent = event.continent()
        try:
            query = "INSERT INTO continent (continent_code, name) VALUES (?, ?)"
            cursor = self._conn.cursor()
            cursor.execute(query, (_continent.continent_code, _continent.name))
            self._conn.commit()
            cursor.close()
            yield ContinentSavedEvent(_continent)
        except sqlite3.Error as e:
            yield SaveContinentFailedEvent(str(e))

    def save_continent(self, event):
        _continent = event.continent()
        try:
            query = "UPDATE continent SET continent_code = ?, name = ? WHERE continent_id = ?"
            cursor = self._conn.cursor()
            cursor.execute(query, (_continent.continent_code, _continent.name, _continent.continent_id))
            self._conn.commit()
            cursor.close()
            yield ContinentSavedEvent(_continent)
        except sqlite3.Error as e:
            yield SaveContinentFailedEvent(str(e))
