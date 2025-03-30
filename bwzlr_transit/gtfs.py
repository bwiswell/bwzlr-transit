import os
from typing import Any, Callable

from marshmallow import Schema
import pandas as pd

from . import models as m

from .route import Route, ROUTE_SCHEMA
from .schedule import Schedule, SCHEDULE_SCHEMA
from .shape import Shape, SHAPE_SCHEMA
from .stop import Stop, STOP_SCHEMA
from .stop_time import StopTime, STOPTIME_SCHEMA
from .trip import Trip, TRIP_SCHEMA


class GTFS:
    def __init__ (self, name: str, path: str):
        self.name = name
        self.path = path

        self.agency: m.Agency = self._load('agency', m.AGENCY_SCEMA)
        self.feed: Feed = self._load('feed_info', FEED_SCHEMA)[0]

        self.calendar: dict[str, Schedule] = self._load_dict('calendar', SCHEDULE_SCHEMA, lambda cd: cd.service_id)
        self.dates: dict[str, CalDate] = self._load_dict('calendar_dates', CALDATE_SCHEMA, lambda cd: cd.service_id)

        self.routes: dict[str, Route] = self._load_dict('routes', ROUTE_SCHEMA, lambda r: r.id)

        self.shapes: list[Shape] = self._load('shapes', SHAPE_SCHEMA)
        self.stop_times: list[StopTime] = self._load('stop_times', STOPTIME_SCHEMA)
        self.stops: list[Stop] = self._load('stops', STOP_SCHEMA)
        self.trips: list[Trip] = self._load('trips', TRIP_SCHEMA)


    def _load (self, name: str, schema: Schema) -> list:
        df = pd.read_csv(os.path.join(self.path, f'{name}.txt'), dtype=str).fillna('')
        json = df.to_dict(orient='records')
        values = []
        for rec in json:
            values.append(schema.load(rec))
        return values
    
    def _load_dict (self, name: str, schema: Schema, key: Callable[[Any], str]) -> dict:
        values = self._load(name, schema)
        return { key(value): value for value in values }