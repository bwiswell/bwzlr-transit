from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional

from ..models import Agency, AGENCY_SCHEMA

from .util import load_table


@dataclass
class Agencies:
    '''
    A dataclass table mapping `str` IDs to `Agency` records.

    Attributes:
        agencies (list[Agency]): a list of all `Agency` records in the table
        agency_ids (list[str]): a list of all `Agency.id` values in the table
        data (dict[str, Agency]): a dict mapping `str` IDs to `Agency` records
    '''

    ### ATTRIBUTES ###
    _agencies: dict[str, Agency]


    ### MAGIC METHODS ###
    def __getitem__ (self, id: str) -> Optional[Agency]:
        '''
        Returns the `Agency` record associated with `id`.

        Parameters:
            id (str): the agency ID to match against `Agency.id`

        Returns:
            agency (Optional[Agency]): the `Agency` record associated with 
            `id`, or `None` if no matching record exists
        '''
        return self.data.get(id, None)


    ### CLASS METHODS ###
    @classmethod
    def load (cls, dataset_path: str) -> Agencies:
        '''
        Returns an `Agencies` table containing all of the `Agency` records 
        found at `<dataset_path>/agency.txt`.

        Parameters:
            dataset_path (str): the path to the GTFS dataset

        Returns:
            agencies (Agencies): a dataclass table mapping `str` IDs to 
            `Agency` records
        '''
        return Agencies(
            load_table(
                path = os.path.join(dataset_path, 'agency.txt'),
                schema = AGENCY_SCHEMA,
                key_fn = lambda a: a.id
            )
        )


    ### PROPERTIES ###
    @property
    def agencies (self) -> list[Agency]:
        '''a list of all `Agency` records in the table'''
        return list(self._agencies.values())

    @property
    def agency_ids (self) -> list[str]: 
        '''a list of all `Agency.id` values in the table'''
        return list(self._agencies.keys())

    @property
    def data (self) -> dict[str, Agency]: 
        '''a dict mapping `str` IDs to `Agency` records'''
        return self._agencies


    ### METHODS ###
    def find (self, name: str) -> Optional[Agency]:
        '''
        Returns the `Agency` record associated with `name`.

        Parameters:
            name (str): the agency name to match against `Agency.name`

        Returns:
            agency (Optional[Agency]): the `Agency` record associated with 
            `name`, or `None` if no matching record exists
        '''
        for agency in self.agencies:
            if agency.name == name: 
                return agency