from dataclasses import dataclass
from enum import Enum
from typing import Optional

import desert as d
import marshmallow as m

from .stop_continuity import StopContinuity


class TransitType(Enum):
    '''
    An `Enum` describing the transit type of a route.
    '''
    LIGHT_RAIL = 0
    SUBWAY = 1
    RAIL = 2
    BUS = 3
    FERRY = 4
    CABLE_TRAM = 5
    CABLE_CAR = 6
    FUNICULAR = 7
    TROLLEYBUS = 11
    MONORAIL = 12


@dataclass
class Route:
    '''
    A GTFS dataclass model for records found in `routes.txt`. Identifies a 
    transit route.
    
    Attributes:
        id (str):
            the unique ID of the route
        agency_id (str):
            the unique ID of the agency the route belongs to
        network_id (Optional[str]):
            the unique ID of the network the route belongs to
        color (str):
            the color associated with the route
        desc (Optional[str]):
            a description of the route
        dropoffs (StopContinuity):
            the continuity of dropoffs along the route
        long_name (Optional[str]):
            the full name of the route
        name (str):
            the name of the route
        pickups (StopContinuity):
            the continuity of pickups along the route
        short_name (Optional[str]):
            the short name of the route
        sort_idx (int):
            the sort position index of the route
        text_color (str):
            the color to use for text drawn against `Route.color`
        type (TransitType):
            the `TransitType` of the route
        url (Optional[str]):
            the URL of a web page about the route
    '''

    ### ATTRIBUTES ###
    # Model ID
    id: str = d.field(m.fields.String(data_key='route_id'))
    '''the unique ID of the route'''
    
    # Foreign IDs
    agency_id: str = d.field(
        m.fields.String(data_key='agency_id', missing='')
    )
    '''the unique ID of the agency the route belongs to'''
    network_id: Optional[str] = d.field(
        m.fields.String(data_key='network_id', missing=None)
    )
    '''the unique ID of the network the route belongs to'''

    # Required fields
    color: str = d.field(
        m.fields.String(data_key='route_color', missing='FFFFFF')
    )
    '''the color associated with the route'''
    dropoffs: StopContinuity = d.field(
        m.fields.Enum(
            StopContinuity, by_value=True, missing=StopContinuity.NONE
        )
    )
    '''the continuity of dropoffs along the route'''
    pickups: StopContinuity = d.field(
        m.fields.Enum(
            StopContinuity, by_value=True, missing=StopContinuity.NONE
        )
    )
    '''the continuity of pickups along the route'''
    sort_idx: int = d.field(
        m.fields.Integer(data_key='route_sort_order', missing=0)
    )
    '''the sort position index of the route'''
    text_color: Optional[str] = d.field(
        m.fields.String(data_key='route_text_color', missing='000000')
    )
    '''the color to use for text drawn against `Route.color`'''
    type: TransitType = d.field(
        m.fields.Function(
            deserialize=lambda t: TransitType(int(t)), 
            data_key='route_type'
        )
    )
    '''the `TransitType` of the route'''

    # Optional fields
    desc: Optional[str] = d.field(
        m.fields.String(data_key='route_desc', missing=None)
    )
    '''a description of the route'''
    long_name: Optional[str] = d.field(
        m.fields.String(data_key='route_long_name', missing=None)
    )
    '''the full name of the route'''
    short_name: Optional[str] = d.field(
        m.fields.String(data_key='route_short_name', missing=None)
    )
    '''the short name of the route'''
    url: Optional[str] = d.field(
        m.fields.String(data_key='route_url', missing=None)
    )
    '''the URL of a web page about the route'''


    ### PROPERTIES ###
    @property
    def name (self) -> str:
        '''the name of the route'''
        return self.short_name if self.long_name is None else self.long_name


ROUTE_SCHEMA = d.schema(Route)