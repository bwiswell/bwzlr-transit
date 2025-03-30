from __future__ import annotations

from dataclasses import dataclass
from datetime import date as pydate, time
import os
from typing import Callable

from marshmallow import Schema

from .models import gtfs as g, helpers as h


@dataclass
class GTFS:
    '''
    Base dataclass for reading and managing GTFS datasets.
    
    Attributes:
        agencies (dict[str, Agency]):
            a dict mapping `str` IDs to `Agency` records
        feed (Feed):
            the `Feed` of the GTFS dataset
        name (str):
            the name of the GTFS dataset
        path (str):
            the path to the GTFS dataset
        routes (dict[str, Route]):
            a dict mapping `str` IDs to `Route` records
        schedules (dict[str, Schedule]):
            a dict mapping `str` IDs to `Schedule` records
        trips (dict[str, Trip]):
            a dict mapping `str` IDs to `Trip` records
    '''

    ### ATTRIBUTES ###
    # Required fields
    agencies: dict[str, g.Agency]
    '''a dict mapping `str` IDs to `Agency` records'''
    feed: g.Feed
    '''the `Feed` of the GTFS dataset'''
    name: str
    '''the name of the GTFS dataset'''
    path: str
    '''the path to the GTFS dataset'''
    routes: dict[str, g.Route]
    '''a dict mapping `str` IDs to `Route` records'''
    schedules: dict[str, h.Schedule]
    '''a dict mapping `str` IDs to `Schedule` records'''
    trips: dict[str, h.Trip]
    '''a dict mapping `str` IDs to `Trip` records'''


    ### CLASS METHODS ###
    @classmethod
    def load (cls, name: str, path: str) -> GTFS:
        print('loading agencies...')
        agencies = {
            a.id: a for a in GTFS.load_list(
                os.path.join(path, 'agency.txt'), g.AGENCY_SCHEMA
            )
        }
        print('loading feed info...')
        feed = GTFS.load_list(
            os.path.join(path, 'feed_info.txt'), g.FEED_SCHEMA
        )[0]
        print('loading routes...')
        routes = {
            r.id: r for r in GTFS.load_list(
                os.path.join(path, 'routes.txt'), g.ROUTE_SCHEMA
            )
        }
        print('loading schedules...')
        calendars: list[g.Calendar] = GTFS.load_list(
            os.path.join(path, 'calendar.txt'), g.CALENDAR_SCHEMA
        )
        dates: list[g.CalendarDate] = GTFS.load_list(
            os.path.join(path, 'calendar_dates.txt'), g.CALENDAR_DATE_SCHEMA
        )
        service_ids = set(
            [c.service_id for c in calendars] + [d.service_id for d in dates]
        )
        schedules = {
            sid: h.Schedule(
                additions=[
                    d for d in dates 
                    if d.exception == g.ExceptionType.ADD and \
                        d.service_id == sid
                ],
                calendars=[c for c in calendars if c.service_id == sid],
                exceptions=[
                    d for d in dates
                    if d.exception == g.ExceptionType.REMOVE and \
                        d.service_id == sid
                ]
            ) for sid in service_ids
        }
        print('loading stop times...')
        stop_times: list[g.StopTime] = GTFS.load_list(
            os.path.join(path, 'stop_times.txt'), g.STOP_TIME_SCHEMA
        )
        print('loading trips...')
        trips: list[g.Trip] = [
            h.Trip.from_gtfs(trip, stop_times) for trip in GTFS.load_list(
                os.path.join(path, 'trips.txt'), g.TRIP_SCHEMA
            )
        ]

        return GTFS(
            agencies=agencies, 
            feed=feed, 
            name=name, 
            path=path, 
            routes=routes, 
            schedules=schedules, 
            trips=trips
        )


    @classmethod
    def load_list (cls, path: str, schema: Schema) -> list:
        '''
        Reads a CSV file and returns a list of deserialized records.

        Parameters:
            path (str):
                the path of the CSV file to load data from
            schema (marshmallow.Schema):
                the Schema for the records in the CSV file

        Returns:
            records (list[T]):
                a list of deserialized records
        '''
        print('\treading data from CSV...')
        data: list[str]
        with open(path, 'r') as file:
            data = file.readlines()

        header = data[0].rstrip().split(',')
        print('\tparsing data...')
        records = []
        for line in data[1:]:
            if len(line) == 0: continue
            records.append(
                schema.load({
                    h: v if len(v) > 0 else None
                    for h, v in zip(
                        header,
                        line.rstrip().split(',')
                    )
                })
            )
        return records
    

    ### METHODS ###        
    def filtered (self, filter: Callable[[h.Trip], bool]) -> GTFS:
        '''
        Returns a GTFS dataset filtered according to `filter`

        Parameters:
            filter (Callable[[Trip], bool]):
                the filter to use on the GTFS dataset
        
        Returns:
            gtfs (GTFS):
                a GTFS dataset filtered according to `filter`
        '''
        return GTFS(
            agencies=self.agencies,
            feed=self.feed,
            name=self.name,
            path=self.path,
            routes=self.routes,
            schedules=self.schedules,
            trips={
                trip.id: trip for trip in self.trips.values()
                if filter(trip)
            }
        )
    
    def on (self, date: pydate) -> GTFS:
        '''
        Return a GTFS dataset containing only the trips starting on `date`.

        Parameters:
            date (date):
                the date to filter the GTFS to

        Returns:
            gtfs (GTFS):
                the filtered GTFS dataset
        '''
        return self.filtered(
            lambda t: self.schedules[t.service_id].active(date)
        )