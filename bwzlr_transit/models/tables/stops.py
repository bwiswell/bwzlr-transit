from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional

from ..gtfs import Stop, STOP_SCHEMA
from ..util import load_list


@dataclass
class Stops:
    '''
    A dataclass table mapping `str` IDs to `Stop` records.

    Attributes:
        data (dict[str, Stop]):
            a dict mapping `str` IDs to `Stop` records
        stops (list[Stop]):
            a list of all `Stop` records in the table
        stop_ids (list[str]):
            a list of all `Stop.id` values in the table
    '''

    ### ATTRIBUTES ###
    _stops: dict[str, Stop]


    ### CLASS METHODS ###
    @classmethod
    def load (cls, dataset_path: str) -> Stops:
        '''
        Returns an `Stops` table containing all of the `Stop` records found at 
        `<dataset_path>/stops.txt`.

        Parameters:
            dataset_path (str):
                the path to the GTFS dataset

        Returns:
            stops (Stops):
                a dataclass table mapping `str` IDs to `Stop` records
        '''
        stops: list[Stop] = load_list(
            path=os.path.join(dataset_path, 'stops.txt'),
            schema=STOP_SCHEMA
        )

        return Stops({ s.id: s for s in stops })


    ### MAGIC METHODS ###
    def __getitem__ (self, id: str) -> Optional[Stop]:
        '''
        Returns the `Stop` record associated with `id`.

        Parameters:
            id (str):
                the stop ID to match against `Stop.id`

        Returns:
            stop (Optional[Stop]):
                the `Stop` record associated with `id`, or `None` if no \
                matching record exists
        '''
        return self.data.get(id, None)


    ### PROPERTIES ###
    @property
    def data (self) -> dict[str, Stop]: 
        '''a dict mapping `str` IDs to `Stop` records'''
        return self._stops
    
    @property
    def stops (self) -> list[Stop]:
        '''a list of all `Stop` records in the table'''
        return list(self._stops.values())

    @property
    def stop_ids (self) -> list[str]: 
        '''a list of all `Stop.id` values in the table'''
        return list(self._stops.keys())


    ### METHODS ###
    def find (self, name: str) -> Optional[Stop]:
        '''
        Returns the `Stop` record associated with `name`.

        Parameters:
            name (str):
                the stop name to match against `Stop.name`

        Returns:
            stop (Optional[Stop]):
                the `Stop` record associated with `name`, or `None` if no \
                matching record exists
        '''
        for stop in self.stops:
            if stop.name == name: 
                return stop