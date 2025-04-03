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
        '''
        Returns a `GTFS` object containing minified GTFS data loaded from local
        files or fetched from a remote source.

        If provided, `mgtfs_path` is checked first for a mGTFS dataset. If it
        exists, the `GTFS` object is created from it and returned; otherwise,
        `load` falls back to one of the following:
        
        - loading a unzipped local GTFS dataset at `gtfs_path`
        - fetching a zipped remote GTFS dataset at `gtfs_uri` with an optional \
            `gtfs_sub` for nested GTFS datasets

        If `mgtfs_path` was specified but `load` fell back to a different 
        method, the newly parsed mGTFS will be written to `mgtfs_path` to 
        improve performance on subsequent loads.

        Parameters:
            name (str):
                the name of the GTFS dataset
            gtfs_path (Optional[str]):
                the path to a local GTFS dataset
            gtfs_sub (Optional[str]):
                the subdirectory to use when fetching a remote GTFS dataset
            gtfs_uri (Optional[str]):
                the URI to use when fetching a remote GTFS dataset
            mgtfs_path (Optional[str]):
                the path to a local mGTFS dataset
        
        Returns:
            gtfs (GTFS):
                a `GTFS` object containing the minified GTFS dataset
        '''
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
        '''
        Writes a `GTFS` object to a `.json` file at `mgtfs_path`.

        Parameters:
            gtfs (GTFS):
                the `GTFS` to dump to file
            mgtfs_path (str):
                the `.json` file to dump the `GTFS` object to
        '''
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
    
    def between (self, start: pydate, end: pydate) -> GTFS:
        return self._ref(self.trips.between(start, end))
    
    def connecting (self, stop_a_id: str, stop_b_id: str) -> GTFS:
        '''
        Returns a `GTFS` object containing only the trips connecting the stops
        corresponding to `stop_a_id` and `stop_b_id`.

        Parameters:
            stop_a_id (str):
                the unique ID corresponding to the starting stop
            stop_b_id (str):
                the unique ID corresponding to the ending stop

        Returns:
            gtfs (GTFS)
                a `GTFS` object containing only the trips connecting the stops
                corresponding to `stop_a_id` and `stop_b_id`
        '''
        return self._ref(self.trips.connecting(stop_a_id, stop_b_id))
    
    def on_date (self, date: pydate) -> GTFS:
        '''
        Returns a `GTFS` object containing only the trips occuring on `date`

        Parameters:
            date (date):
                the date to find trips occuring on

        Returns:
            gtfs (GTFS):
                a `GTFS` object containing only the trips occuring on `date`
        '''
        return self._ref(self.trips.on_date(self.schedules.on_date(date)))
    
    def on_route (self, route_id: str) -> GTFS:
        return self._ref(self.trips.on_route(route_id))

    def today (self) -> GTFS:
        '''
        Returns a `GTFS` object containing only the trips occuring on the
        current date.'
        
        Returns:
            gtfs (GTFS):
                a `GTFS` object containing only the trips occuring on the
                current date
        '''
        return self.on_date(pydate.today())

    



GTFS_SCHEMA = d.schema(GTFS)