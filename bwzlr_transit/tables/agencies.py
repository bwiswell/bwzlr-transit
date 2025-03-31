from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional

import desert as d
import marshmallow as m

from ..models import Agency, AGENCY_SCHEMA
from ..util import load_list


@dataclass
class Agencies:
    '''
    Serializable dataclass table mapping `str` IDs to `Agency` records.

    Attributes:
        agencies (list[Agency]):
            a `list` of all `Agency` records in the `Agencies` table
        data (dict[str, Agency]):
            a `dict` mapping `str` IDs to `Agency` records
        ids (list[str]):
            a `list` of all `str` IDs in the `Agencies` table
    '''

    ### ATTRIBUTES ###
    data: dict[str, Agency] = d.field(
        m.fields.Function(
            deserialize=lambda data: { 
                id: AGENCY_SCHEMA.load(d) 
                for id, d in data.items() 
            },
            serialize=lambda data: { 
                d.id: AGENCY_SCHEMA.dump(d) 
                for d in data.data.values() 
            }
        )
    )
    '''a `dict` mapping `str` IDs to `Agency` records'''


    ### CLASS METHODS ###
    @classmethod
    def from_gtfs (cls, path: str) -> Agencies:
        '''
        Returns an `Agencies` table populated from the GTFS data at `path`.

        Parameters:
            path (str):
                the path to the GTFS dataset

        Returns:
            agencies (Agencies):
                an `Agencies` table populated from the GTFS data at `path`
        '''
        agencies: list[Agency] = load_list(
            path = os.path.join(path, 'agency.txt'),
            schema = AGENCY_SCHEMA
        )
        return Agencies({ a.id: a for a in agencies })


    ### PROPERTIES ###
    @property
    def agencies (self) -> list[Agency]:
        '''a `list` of all `Agency` records in the `Agencies` table'''
        return list(self.data.values())
    
    @property
    def ids (self) -> list[str]:
        '''a `list` of all `str` IDs in the `Agencies` table'''
        return list(self.data.keys())
    

    ### MAGIC METHODS ###
    def __getitem__ (self, id: str) -> Optional[Agency]:
        '''
        Returns the `Agency` record associated with the `id` if it exists,
        otherwise returns `None`.
        
        Parameters:
            id (str):
                the `str` id associated with the `Agency` record to retrieve

        Returns:
            record (Optional[Agency]):
                the `Agency` record associated with `id` if it exists, otherwise 
                `None`
        '''
        return self.data.get(id, None)
    

AGENCIES_SCHEMA = d.schema(Agencies)