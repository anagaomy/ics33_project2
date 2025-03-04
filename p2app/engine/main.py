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
from .database import DatabaseManager
from .continents import ContinentManager
from .countries import CountryManager
from .regions import RegionManager


class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self._conn = None
        self.path = None
        self._db_manager = DatabaseManager()
        self._continent_manager = None
        self._country_manager = None
        self._region_manager = None

    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""

        if isinstance(event, QuitInitiatedEvent):
            yield EndApplicationEvent()

        elif isinstance(event, OpenDatabaseEvent):
            yield from self._db_manager.open_database(event)
            self._conn = self._db_manager.connection()
            self.path = self._db_manager.database_path()

        elif isinstance(event, CloseDatabaseEvent):
            yield DatabaseClosedEvent()

        elif isinstance(event, StartContinentSearchEvent):
            self._continent_manager = ContinentManager(self._conn)
            yield from self._continent_manager.start_continent_search(event)

        elif isinstance(event, LoadContinentEvent):
            self._continent_manager = ContinentManager(self._conn)
            yield from self._continent_manager.load_continent(event)

        elif isinstance(event, SaveNewContinentEvent):
            self._continent_manager = ContinentManager(self._conn)
            yield from self._continent_manager.save_new_continent(event)

        elif isinstance(event, SaveContinentEvent):
            self._continent_manager = ContinentManager(self._conn)
            yield from self._continent_manager.save_continent(event)

        elif isinstance(event, StartCountrySearchEvent):
            self._country_manager = CountryManager(self._conn)
            yield from self._country_manager.start_country_search(event)

        elif isinstance(event, LoadCountryEvent):
            self._country_manager = CountryManager(self._conn)
            yield from self._country_manager.load_country(event)

        elif isinstance(event, SaveNewCountryEvent):
            self._country_manager = CountryManager(self._conn)
            yield from self._country_manager.save_new_country(event)

        elif isinstance(event, SaveCountryEvent):
            self._country_manager = CountryManager(self._conn)
            yield from self._country_manager.save_country(event)

        elif isinstance(event, StartRegionSearchEvent):
            self._region_manager = RegionManager(self._conn)
            yield from self._region_manager.start_region_search(event)

        elif isinstance(event, LoadRegionEvent):
            self._region_manager = RegionManager(self._conn)
            yield from self._region_manager.load_region(event)

        elif isinstance(event, SaveNewRegionEvent):
            self._region_manager = RegionManager(self._conn)
            yield from self._region_manager.save_new_region(event)

        elif isinstance(event, SaveRegionEvent):
            self._region_manager = RegionManager(self._conn)
            yield from self._region_manager.save_region(event)

        else:
            yield ErrorEvent(f"ERROR: {event}")
