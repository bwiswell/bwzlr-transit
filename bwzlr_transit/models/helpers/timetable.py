from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..gtfs import StopTime


@dataclass
class Timetable:
    '''
    A dataclass model that defines a timetable for a trip.

    Attributes:
        data (dict[str, StopTime])
            a dict mapping `str` IDs to `StopTime` records
        stops (list[StopTime])
            a list of all `Stop` records in the table
        stop_ids (list[str])
            a list of all `stop_ids` in the table
    '''

    ### ATTRIBUTES ###
    # Required fields
    _stops: dict[str, StopTime]


    ### CLASS METHODS ###
    @classmethod
    def from_gtfs (cls, stops: list[StopTime]) -> Timetable:
        '''
        Returns a `Timetable` created from the given `StopTime` records.

        All `StopTime` values should be for the same trip.

        Parameters:
            stops (list[StopTime])
                a list of `StopTime` records associated with a trip

        Returns:
            timetable (Timetable):
                a dataclass model that defines a timetable for a trip
        '''
        return Timetable({ s.stop_id: s for s in stops })


    ### MAGIC METHODS ###
    def __getitem__ (self, stop_id: str) -> Optional[StopTime]:
        '''
        Returns the `StopTime` record associated with `stop_id`.

        Parameters:
            stop_id (str):
                the service ID to match against `StopTime.stop_id`

        Returns:
            stop (Optional[StopTime]):
                the `StopTime` record associated with `stop_id`, or `None` if \
                no matching record exists
        '''
        return self.data.get(stop_id, None)


    ### PROPERTIES ###   
    @property
    def data (self) -> dict[str, StopTime]:
        '''a dict mapping `str` IDs to `StopTime` records'''
        return self._stops
     
    @property
    def stops (self) -> list[StopTime]:
        '''a list of all `Stop` records in the table'''
        return list(self._stops.values())

    @property
    def stop_ids (self) -> list[str]: 
        '''a list of all `stop_ids` in the table'''
        return list(self._stops.keys())