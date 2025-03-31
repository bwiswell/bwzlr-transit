from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional

import desert as d
import marshmallow as m

from ..models import Route, ROUTE_SCHEMA
from ..util import load_list


@dataclass
class Routes:
    '''
    Serializable dataclass table mapping `str` IDs to `Route` records.

    Attributes:
        data (dict[str, Route]):
            a `dict` mapping `str` IDs to `Route` records
        ids (list[str]):
            a `list` of all `str` IDs in the `Routes` table
        routes (list[Route]):
            a `list` of all `Route` records in the `Routes` table
    '''

    ### ATTRIBUTES ###
    data: dict[str, Route] = d.field(
        m.fields.Function(
            deserialize=lambda data: { 
                id: ROUTE_SCHEMA.load(d) 
                for id, d in data.items() 
            },
            serialize=lambda data: { 
                d.id: ROUTE_SCHEMA.dump(d) 
                for d in data.data.values() 
            }
        )
    )
    '''a `dict` mapping `str` IDs to `Route` records'''


    ### CLASS METHODS ###
    @classmethod
    def from_gtfs (cls, path: str) -> Routes:
        '''
        Returns an `Routes` table populated from the GTFS data at `path`.

        Parameters:
            path (str):
                the path to the GTFS dataset

        Returns:
            agencies (Routes):
                an `Routes` table populated from the GTFS data at `path`
        '''
        routes: list[Route] = load_list(
            path = os.path.join(path, 'routes.txt'),
            schema = ROUTE_SCHEMA,
            int_cols=['route_type']
        )
        return Routes({ r.id: r for r in routes })


    ### PROPERTIES ###    
    @property
    def ids (self) -> list[str]:
        '''a `list` of all `str` IDs in the `Routes` table'''
        return list(self.data.keys())
    
    @property
    def routes (self) -> list[Route]:
        '''a `list` of all `Route` records in the `Routes` table'''
        return list(self.data.values())
    

    ### MAGIC METHODS ###
    def __getitem__ (self, id: str) -> Optional[Route]:
        '''
        Returns the `Route` record associated with the `id` if it exists,
        otherwise returns `None`.
        
        Parameters:
            id (str):
                the `str` id associated with the `Route` record to retrieve

        Returns:
            record (Optional[Route]):
                the `Route` record associated with `id` if it exists, otherwise 
                `None`
        '''
        return self.data.get(id, None)
    

ROUTES_SCHEMA = d.schema(Routes)