from __future__ import annotations

from dataclasses import dataclass
import os

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
        agencies = {
            a.id: a for a in GTFS.load_list(
                os.path.join(path, 'agency.txt'), g.AGENCY_SCHEMA
            )
        }
        feed = GTFS.load_list(
            os.path.join(path, 'feed_info.txt'), g.FEED_SCHEMA
        )[0]
        routes = {
            r.id: r for r in GTFS.load_list(
                os.path.join(path, 'routes.txt'), g.ROUTE_SCHEMA
            )
        }

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

        stop_times: list[g.StopTime] = GTFS.load_list(
            os.path.join(path, 'stop_times.txt'), g.STOP_TIME_SCHEMA
        )
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
        data: list[str]
        with open(path, 'r') as file:
            data = file.readlines()

        header = data[0].rstrip().split(',')
        data = [l.rstrip().split(',') for l in data[1:]]

        return [
            schema.load({ 
                head: val 
                for head, val in zip(header, values) 
            }) for values in data
        ]