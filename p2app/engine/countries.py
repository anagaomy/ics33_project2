# countries.py


import sqlite3
from p2app.events import *


class CountryManager:
    def __init__(self):
        self._conn = None
        self.path = None

    def start_country_search(self, event):
        search_criteria = event.country_code(), event.name()

        if event.country_code() is None or event.name() is None:
            query = "SELECT * FROM country WHERE country_code = ? OR name = ?"
        else:
            query = "SELECT * FROM country WHERE country_code = ? AND name = ?"

        cursor = self._conn.cursor()
        cursor.execute(query, search_criteria)
        _countries = cursor.fetchall()
        cursor.close()
        for country in _countries:
            yield CountrySearchResultEvent(Country(*country))

    def load_country(self, event):
        country_id = event.country_id()
        query = "SELECT * FROM country WHERE country_id = ?"
        cursor = self._conn.cursor()
        cursor.execute(query, (country_id,))
        _country = cursor.fetchone()
        cursor.close()
        if _country:
            yield CountryLoadedEvent(Country(*_country))

    def save_new_country(self, event):
        _country = event.country()
        try:
            query = "INSERT INTO country (country_code, name, continent_id, wikipedia_link) VALUES (?, ?, ?, ?)"
            cursor = self._conn.cursor()
            cursor.execute(query, (_country.country_code, _country.name,
                                   _country.continent_id, _country.wikipedia_link))
            self._conn.commit()
            cursor.close()
            yield CountrySavedEvent(_country)
        except sqlite3.Error as e:
            yield SaveCountryFailedEvent(str(e))

    def save_country(self, event):
        _country = event.country()
        try:
            query = ("UPDATE country SET country_code = ?, name = ?, continent_id = ?, wikipedia_link = ?"
                     "WHERE country_id = ?")
            cursor = self._conn.cursor()
            cursor.execute(query, (_country.country_code, _country.name, _country.continent_id,
                                   _country.wikipedia_link, _country.country_id))
            self._conn.commit()
            cursor.close()
            yield CountrySavedEvent(_country)
        except sqlite3.Error as e:
            yield SaveCountryFailedEvent(str(e))
