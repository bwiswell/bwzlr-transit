from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional

from ..gtfs import (
    Calendar, 
    CalendarDate, 
    CALENDAR_SCHEMA, 
    CALENDAR_DATE_SCHEMA, 
    ExceptionType as ExType
)
from ..helpers import Schedule
from ..util import load_list


@dataclass
class Services:
    '''
    A dataclass table mapping `str` IDs to `Schedule` records.

    Attributes:
        data (dict[str, Schedule]):
            a dict mapping `str` IDs to `Schedule` records
        schedules (list[Schedule]):
            a list of all `Schedule` records in the table
        service_ids (list[str]):
            a list of all `Schedule.service_id` values in the table
    '''

    ### ATTRIBUTES ###
    _schedules: dict[str, Schedule]


    ### CLASS METHODS ###
    @classmethod
    def load (cls, dataset_path: str) -> Services:
        '''
        Returns an `Services` table containing all of the `Schedule` records 
        compiled from the `Calendar` records in `<dataset_path>/calendar.txt` 
        and the `CalendarDate` records in `<dataset_path>/calendar_dates.txt`.

        Parameters:
            dataset_path (str):
                the path to the GTFS dataset

        Returns:
            services (Services):
                a dataclass table mapping `str` IDs to `Schedule` records
        '''
        calendars: list[Calendar] = load_list(
            path = os.path.join(dataset_path, 'calendar.txt'),
            schema = CALENDAR_SCHEMA
        )
        dates: list[CalendarDate] = load_list(
            path = os.path.join(dataset_path, 'calendar_dates.txt'),
            schema = CALENDAR_DATE_SCHEMA
        )

        service_ids = set(
            [c.service_id for c in calendars] + [cd.service_id for cd in dates]
        )

        return Services({
            sid: Schedule(
                additions = [
                    cd for cd in dates 
                    if cd.service_id == sid and cd.exception == ExType.ADD
                ],
                calendars = [c for c in calendars if c.service_id == sid],
                exceptions = [
                    cd for cd in dates
                    if cd.service_id == sid and cd.exception == ExType.REMOVE
                ]
            ) for sid in service_ids
        })


    ### MAGIC METHODS ###
    def __getitem__ (self, id: str) -> Optional[Schedule]:
        '''
        Returns the `Schedule` record associated with `id`.

        Parameters:
            id (str):
                the service ID to match against `Schedule.service_id`

        Returns:
            schedule (Optional[Schedule]):
                the `Schedule` record associated with `id`, or `None` if no \
                matching record exists
        '''
        return self.data.get(id, None)


    ### PROPERTIES ###
    @property
    def data (self) -> dict[str, Schedule]: 
        '''a dict mapping `str` IDs to `Schedule` records'''
        return self._schedules
    
    @property
    def schedules (self) -> list[Schedule]:
        '''a list of all `Schedule` records in the table'''
        return list(self._schedules.values())

    @property
    def service_ids (self) -> list[str]: 
        '''a list of all `Schedule.service_id` values in the table'''
        return list(self._schedules.keys())