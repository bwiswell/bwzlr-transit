from __future__ import annotations

from dataclasses import dataclass

import desert as d
import marshmallow as m

from .models import Feed, FEED_SCHEMA
from .tables import (
    Agencies, AGENCIES_SCHEMA,
    Routes, ROUTES_SCHEMA,
    Schedules, SCHEDULES_SCHEMA,
    Trips, TRIPS_SCHEMA
)


@dataclass
class GTFS:
    '''
    Base dataclass database for reading and managing GTFS datasets.
    
    Attributes:
        agencies (Agencies):
            an `Agencies` table mapping `str` IDs to `Agency` records
        feed (Feed):
            the `Feed` of the GTFS dataset
        name (str):
            the name of the GTFS dataset
        routes (Routes):
            a `Routes` table mapping `str` IDs to `Route` records
        schedules (Schedules):
            a `Schedules` table mapping `str` service IDs to `Schedule` records
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
    trips: Trips = d.field(m.fields.Nested(TRIPS_SCHEMA))
    '''a `Trips` table mapping `str` IDs to `Trip` records'''


GTFS_SCHEMA = d.schema(GTFS)