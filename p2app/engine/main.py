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
        # self._conn = sqlite3.connect('airport.db')
        # self._conn.execute("PRAGMA foreign_keys = ON;")

    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""

        # This is a way to write a generator function that always yields zero values.
        # You'll want to remove this and replace it with your own code, once you start
        # writing your engine, but this at least allows the program to run.
        if isinstance(event, QuitInitiatedEvent):
            yield EndApplicationEvent()
        elif isinstance(event, OpenDatabaseEvent):
            try:
                self._database_path = event.path()
                yield DatabaseOpenedEvent(event.path())
            except Exception as e:
                yield DatabaseOpenFailedEvent(str(e))
        elif isinstance(event, CloseDatabaseEvent):
            self._database_path = None
            yield DatabaseClosedEvent()

        else:
            yield ErrorEvent(f"ERROR: {event}")
