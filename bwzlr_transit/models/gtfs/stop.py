from dataclasses import dataclass
from enum import Enum
from typing import Optional

import desert as d
import marshmallow as m


class Accessibility(Enum):
    '''
    An `Enum` describing the accessibility of a transit location.
    '''
    UNKNOWN = 0
    ACCESSIBLE = 1
    INACCESSIBLE = 2


class LocationType(Enum):
    '''
    An `Enum` describing the nature of a transit location.
    '''
    STOP_OR_PLATFORM = 0
    STATION = 1
    ENTRANCE_OR_EXIT = 2
    GENERIC_NODE = 3
    BOARDING_AREA = 4


@dataclass
class Stop:
    '''
    A GTFS dataclass model for records found in `stops.txt`. Identifies a 
    transit location: a stop/platform, station, entrance/exit, generic node or 
    boarding area (see `LocationType`).

    Attributes:
        id (str):
            the unique ID of the transit location
        level_id (Optional[str]):
            the unique ID of the level of the transit location
        parent_id (Optional[str]):
            the unique ID of the transit location's parent
        zone_id (Optional[str]):
            the unique ID of the fare zone ID of the transit location
        accessibility (Accessibility):
            the `Accessibility` of the transit location for wheelchair \
            boardings
        code (Optional[str]):
            a short text/number identifying the transit location for riders
        desc (Optional[str]):
            a description of the transit location
        lat (Optional[float]):
            the latitude of the transit location
        lon (Optional[float]):
            the longitude of the transit location
        name (str = 'unnamed'):
            the name of the transit location
        platform_code (Optional[str]):
            the unique ID of the platform to stop at
        timezone (Optional[str]):
            the timezone of the transit location
        tts_name (Optional[str]):
            a text-to-speech readable version of the stop name
        type (LocationType):
            the `LocationType` of the transit location
        url (Optional[str]):
            the URL of a web page about the transit location
    '''
    
    ### ATTRIBUTES ###
    # Model ID
    id: str = d.field(m.fields.String(data_key='stop_id'))
    '''the unique ID of the transit location'''

    # Foreign IDs
    level_id: Optional[str] = d.field(
        m.fields.String(data_key='level_id', missing=None)
    )
    '''the unique ID of the level of the transit location'''
    parent_id: Optional[str] = d.field(
        m.fields.String(data_key='parent_station', missing=None)
    )
    '''the unique ID of the transit location's parent'''
    zone_id: Optional[str] = d.field(
        m.fields.String(data_key='zone_id', missing=None)
    )
    '''the unique ID of the fare zone of the transit location'''

    # Required fields
    accessibility: Accessibility = d.field(
        m.fields.Enum(
            Accessibility,
            data_key='wheelchair_boarding',
            by_value=True,
            missing=Accessibility.UNKNOWN
        )
    )
    '''the `Accessibility` of the transit location for wheelchair boardings'''
    type: LocationType = d.field(
        m.fields.Enum(
            LocationType, 
            data_key='location_type', 
            by_value=True,
            missing=LocationType.STOP_OR_PLATFORM
        )
    )
    '''the `LocationType` of the transit location'''

    # Optional fields
    code: Optional[str] = d.field(
        m.fields.String(data_key='stop_code', missing=None)
    )
    '''a short text/number identifying the transit location for riders'''
    desc: Optional[str] = d.field(
        m.fields.String(data_key='stop_desc', missing=None)
    )
    '''a description of the transit location'''
    lat: Optional[float] = d.field(
        m.fields.Float(data_key='stop_lat', missing=None)
    )
    '''the latitude of the transit location'''
    lon: Optional[float] = d.field(
        m.fields.Float(data_key='stop_lon', missing=None)
    )
    '''the longitude of the transit location'''
    name: str = d.field(
        m.fields.String(data_key='stop_name', missing='unnamed')
    )
    '''the name of the transit location'''
    platform_code: Optional[str] = d.field(
        m.fields.String(data_key='platform_code', missing=None)
    )
    '''the unique ID of the platform to stop at'''
    timezone: Optional[str] = d.field(
        m.fields.String(data_key='stop_timezone', missing=None)
    )
    '''the timezone of the transit location'''
    tts_name: Optional[str] = d.field(
        m.fields.String(data_key='tts_stop_name', missing=None)
    )
    '''a text-to-speech readable version of the stop name'''
    url: Optional[str] = d.field(
        m.fields.String(data_key='stop_url', missing=None)
    )
    '''the URL of a web page about the transit location'''


STOP_SCHEMA = d.schema(Stop)