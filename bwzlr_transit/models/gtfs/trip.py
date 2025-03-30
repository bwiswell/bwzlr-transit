from dataclasses import dataclass
from enum import Enum
from typing import Optional

import desert as d
import marshmallow as m

from .accessibility import Accessibility


class BikesAllowed(Enum):
    '''
    An `Enum` indicating if bikes are allowed on a trip.
    '''
    UNKNOWN = 0
    ALLOWED = 1
    DISALLOWED = 2


@dataclass
class Trip:
    '''
    A GTFS dataclass model for records found in `routes.txt`. Identifies a 
    transit route.
    
    Attributes:
        id (str):
            the unique ID of the trip
        block_id (Optional[str]):
            the unique ID of the block the trip belongs to
        route_id (str):
            the unique ID of the route the trip belongs to
        service_id (str):
            the unique ID of the service the trip belongs to
        shape_id (Optional[str]):
            the unique ID of the shape for the trip
        accessibility (Accessibility):
            the `Accessibility` of the trip
        bikes (BikesAllowed):
            the `BikesAllowed` of the trip
        direction (Optional[bool]):
            the direction of the trip
        headsign (Optional[str]):
            the headsign to display for the trip
        short_name (Optional[str]):
            a short name for the trip
    '''

    ### ATTRIBUTES ###
    # Model ID
    id: str = d.field(m.fields.String(data_key='trip_id'))
    '''the unique ID of the trip'''

    # Foreign IDs
    block_id: Optional[str] = d.field(
        m.fields.String(data_key='block_id', missing=None)
    )
    '''the unique ID of the block the trip belongs to'''
    route_id: str = d.field(m.fields.String(data_key='route_id'))
    '''the unique ID of the route the trip belongs to'''
    service_id: str = d.field(m.fields.String(data_key='service_id'))
    '''the unique ID of the service the trip belongs to'''
    shape_id: Optional[str] = d.field(
        m.fields.String(data_key='shape_id', missing=None)
    )
    '''the unique ID of the shape for the trip'''

    # Required fields
    accessibility: Accessibility = d.field(
        m.fields.Function(
            deserialize=lambda a: Accessibility(int(a)),
            data_key='wheelchair_accessible',
            missing=Accessibility.UNKNOWN
        )
    )
    '''the `Accessibility` of the trip'''
    bikes: BikesAllowed = d.field(
        m.fields.Function(
            deserialize=lambda ba: BikesAllowed(int(ba)),
            data_key='bikes_allowed',
            load_default=BikesAllowed.UNKNOWN,
            missing=None,
            required=False
        )
    )
    '''the `BikesAllowed` of the trip'''

    # Optional fields
    direction: Optional[bool] = d.field(
        m.fields.Boolean(data_key='direction_id', missing=None)
    )
    '''the direction of the trip'''
    headsign: Optional[str] = d.field(
        m.fields.String(data_key='trip_headsign', missing=None)
    )
    '''the headsign to display for the trip'''
    short_name: Optional[str] = d.field(
        m.fields.String(data_key='trip_short_name', missing=None)
    )
    '''a short name for the trip'''



TRIP_SCHEMA = d.schema(Trip)