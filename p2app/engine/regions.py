# regions.py


import sqlite3
from p2app.events import *


class RegionManager:
    def __init__(self, connection):
        self._conn = connection

    def start_region_search(self, event):
        search_criteria = []
        conditions = []

        if event.region_code() is not None:
            search_criteria.append(event.region_code())
            conditions.append("region_code = ?")
        if event.local_code() is not None:
            search_criteria.append(event.local_code())
            conditions.append("local_code = ?")
        if event.name() is not None:
            search_criteria.append(event.name())
            conditions.append("name = ?")

        where_clause = " AND ".join(conditions)
        if where_clause:
            query = f"SELECT * FROM region WHERE {where_clause}"
        else:
            query = "SELECT * FROM region"

        cursor = self._conn.cursor()
        cursor.execute(query, search_criteria)
        _regions = cursor.fetchall()
        cursor.close()
        for region in _regions:
            yield RegionSearchResultEvent(Region(*region))

    def load_region(self, event):
        region_id = event.region_id()
        query = "SELECT * FROM region WHERE region_id = ?"
        cursor = self._conn.cursor()
        cursor.execute(query, (region_id,))
        _regions = cursor.fetchall()
        cursor.close()
        for _region in _regions:
            yield RegionLoadedEvent(Region(*_region))

    def save_new_region(self, event):
        _region = event.region()
        try:
            query = ("INSERT INTO region (region_code, local_code, name, continent_id, country_id)"
                     "VALUES (?, ?, ?, ?, ?)")
            cursor = self._conn.cursor()
            cursor.execute(query, (_region.region_code, _region.local_code, _region.name,
                                   _region.continent_id, _region.country_id))
            self._conn.commit()
            cursor.close()
            yield RegionSavedEvent(_region)
        except sqlite3.Error as e:
            yield SaveRegionFailedEvent(str(e))

    def save_region(self, event):
        _region = event.region()
        try:
            query = ("UPDATE region SET region_code = ?, local_code = ?, name = ?, continent_id = ?, country_id = ?"
                     "WHERE region_id = ?")
            cursor = self._conn.cursor()
            cursor.execute(query, (_region.region_code, _region.local_code, _region.name, _region.continent_id,
                                   _region.country_id, _region.region_id))
            self._conn.commit()
            cursor.close()
            yield RegionSavedEvent(_region)
        except sqlite3.Error as e:
            yield SaveRegionFailedEvent(str(e))
