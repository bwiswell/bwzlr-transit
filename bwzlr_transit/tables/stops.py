from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional

import desert as d
import marshmallow as m

from ..models import (
    Stop, STOP_SCHEMA
)
from ..util import load_list


@dataclass
class Stops:
    '''
    Serializable dataclass table mapping `str` IDs to `Stop` records.

    Attributes:
        data (dict[str, Stop]):
            a `dict` mapping `str` IDs to `Stop` records
        ids (list[str]):
            a `list` of all `str` IDs in the `Stops` table
        names (list[str]):
            a `list` of all `Stop.name` values in the `Stops` table
        stops (list[Stop]):
            a `list` of all `Stop` records in the `Stops` table
    '''

    ### ATTRIBUTES ###
    data: dict[str, Stop] = d.field(
        m.fields.Function(
            deserialize=lambda data: { 
                id: STOP_SCHEMA.load(d) 
                for id, d in data.items() 
            },
            serialize=lambda data: { 
                d.id: STOP_SCHEMA.dump(d) 
                for d in data.data.values() 
            }
        )
    )
    '''a `dict` mapping `str` IDs to `Stop` records'''


    ### CLASS METHODS ###
    @classmethod
    def from_gtfs (cls, path: str) -> Stops:
        '''
        Returns an `Stops` table populated from the GTFS data at `path`.

        Parameters:
            path (str):
                the path to the GTFS dataset

        Returns:
            stops (Stops):
                an `Stops` table populated from the GTFS data at `path`
        '''
        stops: list[Stop] = load_list(
            os.path.join(path, 'stops.txt'), 
            STOP_SCHEMA,
            int_cols=['drop_off_type', 'pickup_type', 'timepoint']
        )

        return Stops({ s.id: s for s in stops })


    ### PROPERTIES ###    
    @property
    def ids (self) -> list[str]:
        '''a `list` of all `str` IDs in the `Stops` table'''
        return list(self.data.keys())
    
    @property
    def names (self) -> list[str]:
        '''a `list` of all `Stop.name` values in the `Stops` table'''
        return [s.name for s in self.stops]
    
    @property
    def stops (self) -> list[Stop]:
        '''a `list` of all `Stop` records in the `Stops` table'''
        return list(self.data.values())
    

    ### MAGIC METHODS ###
    def __getitem__ (self, id: str) -> Optional[Stop]:
        '''
        Returns the `Stop` record associated with the `id` if it exists,
        otherwise returns `None`.
        
        Parameters:
            id (str):
                the `str` id associated with the `Stop` record to retrieve

        Returns:
            record (Optional[Stop]):
                the `Stop` record associated with `id` if it exists, otherwise 
                `None`
        '''
        return self.data.get(id, None)
    

STOPS_SCHEMA = d.schema(Stops)