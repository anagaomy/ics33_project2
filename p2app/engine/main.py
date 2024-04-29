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

        # This is a way to write a generator function that always yields zero values.
        # You'll want to remove this and replace it with your own code, once you start
        # writing your engine, but this at least allows the program to run.
        if isinstance(event, QuitInitiatedEvent):
            yield EndApplicationEvent()
        elif isinstance(event, OpenDatabaseEvent):
            yield from self._open_database_event(event)
        elif isinstance(event, CloseDatabaseEvent):
            self._database_path = None
            yield DatabaseClosedEvent()

        elif isinstance(event, StartContinentSearchEvent):
            yield from self._start_continent_search(event)


        else:
            yield ErrorEvent(f"ERROR: {event}")

    def _open_database_event(self, event):
        try:
            self._database_path = event.path()
            self._connect_to_database()
            yield DatabaseOpenedEvent(event.path())
        except Exception as e:
            yield DatabaseOpenFailedEvent(str(e))

    def _start_continent_search(self, event):
        search_criteria = event.continent_code(), event.name()
        query = "SELECT * FROM continent WHERE continent_code=? OR name=?"
        cursor = self._conn.cursor()
        cursor.execute(query, search_criteria)
        _continents = cursor.fetchall()
        cursor.close()
        for continent in _continents:
            yield ContinentSearchResultEvent(Continent(*continent))
