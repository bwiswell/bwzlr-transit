from __future__ import annotations

from dataclasses import dataclass
from datetime import date as pydate
import json
import os
import shutil
from typing import Optional
from urllib import request
import zipfile

import desert as d
import marshmallow as m

from .models import Feed, FEED_SCHEMA
from .tables import (
    Agencies, AGENCIES_SCHEMA,
    Routes, ROUTES_SCHEMA,
    Schedules, SCHEDULES_SCHEMA,
    Stops, STOPS_SCHEMA,
    Trips, TRIPS_SCHEMA
)


TMP = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'tmp')


@dataclass
class GTFS:
    '''
    Base dataclass database for reading and managing GTFS datasets.
    
    Attributes:
        name (str):
            the name of the GTFS dataset
        feed (Feed):
            the `Feed` of the GTFS dataset
        agencies (Agencies):
            an `Agencies` table mapping `str` IDs to `Agency` records
        routes (Routes):
            a `Routes` table mapping `str` IDs to `Route` records
        schedules (Schedules):
            a `Schedules` table mapping `str` service IDs to `Schedule` records
        stops (Stops):
            a `Stops` table mapping `str` IDs to `Stop` records
        trips (Trips):
            a `Trips` table mapping `str` IDs to `Trip` records
    '''

    ### ATTRIBUTES ###
    # Metadata
    name: str = d.field(m.fields.String())
    '''the name of the GTFS dataset'''
    feed: Feed = d.field(m.fields.Nested(FEED_SCHEMA))
    '''a `Feed` record describing the GTFS dataset'''

    # Tables
    agencies: Agencies = d.field(m.fields.Nested(AGENCIES_SCHEMA))
    '''an `Agencies` table mapping `str` IDs to `Agency` records'''
    routes: Routes = d.field(m.fields.Nested(ROUTES_SCHEMA))
    '''a `Routes` table mapping `str` IDs to `Route` records'''
    schedules: Schedules = d.field(m.fields.Nested(SCHEDULES_SCHEMA))
    '''a `Schedules` table mapping `str` service IDs to `Schedule` records'''
    stops: Stops = d.field(m.fields.Nested(STOPS_SCHEMA))
    '''a `Stops` table mapping `str` IDs to `Stop` records'''
    trips: Trips = d.field(m.fields.Nested(TRIPS_SCHEMA))
    '''a `Trips` table mapping `str` IDs to `Trip` records'''


    ### CLASS METHODS ###
    @classmethod
    def load (
                cls,
                name: str,
                gtfs_path: Optional[str] = None,
                gtfs_sub: Optional[str] = None,
                gtfs_uri: Optional[str] = None,
                mgtfs_path: Optional[str] = None
            ) -> GTFS:
        
        if mgtfs_path and os.path.exists(mgtfs_path):
            data = {}
            with open(mgtfs_path, 'r') as file:
                data = json.load(file)
            return GTFS_SCHEMA.load(data)
        
        if not gtfs_path:
            if os.path.exists(TMP): shutil.rmtree(TMP)
            os.mkdir(TMP)
            zip_path = os.path.join(TMP, f'{name}.zip')
            request.urlretrieve(gtfs_uri, zip_path)
            with zipfile.ZipFile(zip_path) as zip:
                zip.extractall(TMP)
            os.remove(zip_path)
            if gtfs_sub:
                zip_name = f'{gtfs_sub}.zip'
                zip_path = os.path.join(TMP, zip_name)
                for entry in os.scandir(TMP):
                    if entry.name != zip_name:
                        os.remove(entry.path)            
                with zipfile.ZipFile(zip_path) as zip:
                    zip.extractall(TMP)
                os.remove(zip_path)
            path = TMP
        else:
            path = gtfs_path

        g = GTFS(
            name=name, 
            feed=Feed.from_gtfs(path),
            agencies=Agencies.from_gtfs(path), 
            routes=Routes.from_gtfs(path), 
            schedules=Schedules.from_gtfs(path),
            stops=Stops.from_gtfs(path),
            trips=Trips.from_gtfs(path)
        )

        if not gtfs_path: shutil.rmtree(TMP)
        if mgtfs_path: GTFS.save(g, mgtfs_path)

        return g


    @classmethod
    def save (cls, gtfs: GTFS, mgtfs_path: str):
        data = GTFS_SCHEMA.dump(gtfs)
        with open(mgtfs_path, 'w') as file:
            json.dump(data, file)


    ### METHODS ###
    def _ref (self, trips: Trips) -> GTFS:
        return GTFS(
            self.name,
            self.feed,
            self.agencies,
            self.routes,
            self.schedules,
            self.stops,
            trips
        )
    
    def connecting (self, stop_a_id: str, stop_b_id: str) -> GTFS:
        return self._ref(self.trips.connecting(stop_a_id, stop_b_id))
    
    def on_date (self, date: pydate) -> GTFS:
        return self._ref(self.trips.on_date(self.schedules.on_date(date)))

    def today (self) -> GTFS:
        return self.on_date(pydate.today())

    



GTFS_SCHEMA = d.schema(GTFS)