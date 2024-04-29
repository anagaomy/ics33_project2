# p2app/engine/main.py
#
# ICS 33 Spring 2024
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.


import sqlite3
from p2app.events import *


class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self._database_path = None
        self._conn = None

    def _connect_to_database(self):
        """Connects to the database and enables foreign key constraints"""
        if self._conn is not None:
            self._conn.close()
        self._conn = sqlite3.connect(self._database_path)
        self._conn.execute("PRAGMA foreign_keys = ON;")

    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""

        if isinstance(event, QuitInitiatedEvent):
            yield EndApplicationEvent()
        elif isinstance(event, OpenDatabaseEvent):
            yield from self._open_database_event(event)
        elif isinstance(event, CloseDatabaseEvent):
            yield from self._close_database_event(event)

        elif isinstance(event, StartContinentSearchEvent):
            yield from self._start_continent_search(event)

        elif isinstance(event, LoadContinentEvent):
            yield from self._load_continent(event)

        elif isinstance(event, SaveNewContinentEvent):
            yield from self._save_new_continent(event)

        else:
            yield ErrorEvent(f"ERROR: {event}")

    def _open_database_event(self, event):
        try:
            self._database_path = event.path()
            self._connect_to_database()
            yield DatabaseOpenedEvent(event.path())
        except sqlite3.Error as e:
            yield DatabaseOpenFailedEvent(str(e))

    def _close_database_event(self, event):
        self._database_path = None
        yield DatabaseClosedEvent()

    def _start_continent_search(self, event):
        search_criteria = event.continent_code(), event.name()
        query = "SELECT * FROM continent WHERE continent_code = ? OR name = ?"
        cursor = self._conn.cursor()
        cursor.execute(query, search_criteria)
        _continents = cursor.fetchall()
        cursor.close()
        for continent in _continents:
            yield ContinentSearchResultEvent(Continent(*continent))

    def _load_continent(self, event):
        continent_id = event.continent_id()
        query = "SELECT * FROM continent WHERE continent_id = ?"
        cursor = self._conn.cursor()
        cursor.execute(query, (continent_id,))
        _continent = cursor.fetchone()
        cursor.close()
        if _continent:
            yield ContinentLoadedEvent(Continent(*_continent))

    def _save_new_continent(self, event):
        _continent = event.continent()
        try:
            query = "INSERT INTO continent (conitent_code, name) VALUES (?, ?)"
            cursor = self._conn.cursor()
            cursor.execute(query, (_continent.continent_code, _continent.name))
            self._conn.commit()
            cursor.close()
            yield ContinentSavedEvent(_continent)
        except sqlite3.Error as e:
            yield SaveContinentFailedEvent(str(e))

    # def _save_continent(self, event):
