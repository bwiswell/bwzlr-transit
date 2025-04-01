from __future__ import annotations

from dataclasses import dataclass
from datetime import date as pydate
import os
from typing import Optional

import desert as d
import marshmallow as m

from ..models import (
    Calendar, CALENDAR_SCHEMA,
    CalendarDate, CALENDAR_DATE_SCHEMA,
    Schedule, SCHEDULE_SCHEMA
)
from ..util import load_list


@dataclass
class Schedules:
    '''
    Serializable dataclass table mapping `str` service IDs to `Schedule`
    records.

    Attributes:
        data (dict[str, Schedule]):
            a `dict` mapping `str` service IDs to `Schedule` records
        schedules (list[Schedule]):
            a `list` of all `Schedule` records in the `Schedules` table
        service_ids (list[str]):
            a `list` of all `str` service IDs in the `Schedules` table
    '''

    ### ATTRIBUTES ###
    data: dict[str, Schedule] = d.field(
        m.fields.Function(
            deserialize=lambda data: { 
                id: SCHEDULE_SCHEMA.load(d) 
                for id, d in data.items() 
            },
            serialize=lambda data: { 
                d.service_id: SCHEDULE_SCHEMA.dump(d) 
                for d in data.data.values()
            }
        )
    )
    '''a `dict` mapping `str` service IDs to `Schedule` records'''


    ### CLASS METHODS ###
    @classmethod
    def from_gtfs (cls, path: str) -> Schedules:
        '''
        Returns an `Schedules` table populated from the GTFS data at `path`.

        Parameters:
            path (str):
                the path to the GTFS dataset

        Returns:
            agencies (Schedules):
                an `Schedules` table populated from the GTFS data at `path`
        '''
        schedules: dict[str, tuple[list[Calendar], list[CalendarDate]]] = {}

        calendars: list[Calendar] = load_list(
            path = os.path.join(path, 'calendar.txt'), 
            schema = CALENDAR_SCHEMA
        )

        for cal in calendars:
            if cal.service_id in schedules:
                schedules[cal.service_id][0].append(cal)
            else:
                schedules[cal.service_id] = ([cal], [])

        dates: list[CalendarDate] = load_list(
            path = os.path.join(path, 'calendar_dates.txt'), 
            schema = CALENDAR_DATE_SCHEMA,
            int_cols = ['exception_type']
        )

        for date in dates:
            if date.service_id in schedules:
                schedules[date.service_id][1].append(date)
            else:
                schedules[date.service_id] = ([], [date])

        return Schedules({
            sid: Schedule.from_gtfs(sid, *schedules[sid])
            for sid in schedules.keys()
        })


    ### PROPERTIES ###
    @property
    def schedules (self) -> list[Schedule]:
        '''a `list` of all `Schedule` records in the `Schedules` table'''
        return list(self.data.values())
    
    @property
    def service_ids (self) -> list[str]:
        '''a `list` of all `str` service IDs in the `Schedules` table'''
        return list(self.data.keys())
    

    ### MAGIC METHODS ###
    def __getitem__ (self, service_id: str) -> Optional[Schedule]:
        '''
        Returns the `Schedule` record associated with the `service_id` if it
        exists, otherwise returns `None`.
        
        Parameters:
            service_id (str):
                the `str` service_id associated with the `Schedule` record to
                retrieve

        Returns:
            record (Optional[Schedule]):
                the `Schedule` record associated with `service_id` if it
                exists, otherwise `None`
        '''
        return self.data.get(service_id, None)
    

    ### METHODS ###
    def on_date (self, date: pydate) -> list[str]:
        return [
            sid for sid in self.service_ids
            if self[sid].active(date)
        ]
    

SCHEDULES_SCHEMA = d.schema(Schedules)