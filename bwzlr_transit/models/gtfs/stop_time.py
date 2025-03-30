from __future__ import annotations

from dataclasses import dataclass
from datetime import time
from enum import Enum
from typing import Optional

import desert as d
import marshmallow as m

from .stop_continuity import StopContinuity


class StopType(Enum):
    '''
    An `Enum` describing the type of the stop.
    '''
    SCHEDULED = 0
    NONE = 1
    VIA_PHONE = 2
    VIA_DRIVER = 3


class Timepoint(Enum):
    '''
    An `Enum` indicating if a stop time is exact or approximate.
    '''
    APPROXIMATE = 0
    EXACT = 1


@dataclass
class StopTime:
    '''
    A GTFS dataclass model for records found in `stop_times.txt`. Identifies a 
    transit route.

    Attributes:
        index (int):
            the sequence index of the stop
        dropoff_booking_id (Optional[str]):
            the unique ID of the dropoff booking rule for the stop
        location_id (Optional[str]):
            the unique ID of the GeoJSON location for the stop
        location_group_id (Optional[str]):
            the unique ID of the location group the stop belongs to
        pickup_booking_id (Optional[str]):
            the unique ID of the pickup booking rule for the stop
        stop_id (Optional[str]):
            the unique ID of the serviced stop
        trip_id (str):
            the unique ID of the trip including the stop
        arrival_time (Optional[str]):
            the arrival time at the stop
        departure_time (Optional[str]):
            the departure time from the stop
        dist_traveled (Optional[float]):
            the distance traveled from the first stop until this stop
        dropoff_continuity (Optional[StopContinuity]):
            the `StopContinuity` for dropoffs at the stop
        dropoff_type (Optional[StopType]):
            the `StopType` for dropoffs at the stop
        end_time (time):
            the end time of the stop
        end_offset (bool):
            a `bool` indicating if the stop date should be offset
        end_pickup_dropoff (Optional[str]):
            the end time for pickup and dropoff
        headsign (Optional[str]):
            the headsign to display when this stop is the destination
        pickup_continuity (Optional[StopContinuity]):
            the `StopContinuity` for pickups at the stop
        pickup_type (Optional[StopType]):
            the `StopType` for pickups at the stop
        start_offset (bool):
            a `bool` indicating if the start date should be offset
        start_pickup_dropoff (Optional[str]):
            the start time for pickup and dropoff
        start_time (time):
            the start time of the stop
        timepoint (Timepoint):
            the timepoint of the stop
    '''

    ### ATTRIBUTES ###
    # Foreign IDs
    dropoff_booking_id: Optional[str] = d.field(
        m.fields.String(data_key='dropoff_booking_rule_id', missing=None)
    )
    '''the unique ID of the pickup booking rule for the stop'''
    location_id: Optional[str] = d.field(
        m.fields.String(data_key='location_id', missing=None)
    )
    '''the unique ID of the GeoJSON location for the stop'''
    location_group_id: Optional[str] = d.field(
        m.fields.String(data_key='location_group_id', missing=None)
    )
    '''the unique ID of the location group the stop belongs to'''
    pickup_booking_id: Optional[str] = d.field(
        m.fields.String(data_key='pickup_booking_rule_id', missing=None)
    )
    '''the unique ID of the pickup booking rule for the stop'''
    stop_id: Optional[str] = d.field(
        m.fields.String(data_key='stop_id', missing=None)
    )
    '''the unique ID of the serviced stop'''
    trip_id: str = d.field(m.fields.String(data_key='trip_id'))
    '''the unique ID of the trip including the stop'''

    # Required fields
    index: int = d.field(m.fields.Integer(data_key='stop_sequence'))
    '''the sequence index of the stop'''
    timepoint: Timepoint = d.field(
        m.fields.Enum(
            Timepoint, 
            by_value=True, 
            data_key='timepoint', 
            missing=Timepoint.EXACT
        )
    )
    '''the timepoint of the stop'''

    # Optional fields
    arrival_time: Optional[str] = d.field(
        m.fields.String(data_key='arrival_time', missing=None)
    )
    '''the arrival time at the stop'''
    departure_time: Optional[str] = d.field(
        m.fields.String(data_key='departure_time', missing=None)
    )
    '''the departure time at the stop'''
    dist_traveled: Optional[float] = d.field(
        m.fields.Float(data_key='shape_dist_traveled', missing=None)
    )
    '''the distance traveled from the first stop until this stop'''
    dropoff_continuity: Optional[StopContinuity] = d.field(
        m.fields.Enum(
            StopContinuity,
            by_value=True,
            data_key='dropoff_pickup',
            missing=None
        )
    )
    '''the `StopContinuity` for dropoffs at the stop'''
    dropoff_type: Optional[StopType] = d.field(
        m.fields.Enum(
            StopType, 
            by_value=True, 
            data_key='drop_off_type', 
            missing=None
        )
    )
    '''the `StopType` for dropoffs at the stop'''
    end_pickup_dropoff: Optional[str] = d.field(
        m.fields.String(data_key='end_pickup_drop_off_window', missing=None)
    )
    '''the end time for pickup and dropoff'''
    headsign: Optional[str] = d.field(
        m.fields.String(data_key='stop_headsign', missing=None)
    )
    '''the headsign to display when this stop is the destination'''
    pickup_continuity: Optional[StopContinuity] = d.field(
        m.fields.Enum(
            StopContinuity,
            by_value=True,
            data_key='continuous_pickup',
            missing=None
        )
    )
    '''the `StopContinuity` for pickups at the stop'''
    pickup_type: Optional[StopType] = d.field(
        m.fields.Enum(
            StopType, 
            by_value=True, 
            data_key='pickup_type', 
            missing=None
        )
    )
    '''the `StopType` for pickups at the stop'''
    start_pickup_dropoff: Optional[str] = d.field(
        m.fields.String(data_key='start_pickup_drop_off_window', missing=None)
    )
    '''the start time for pickup and dropoff'''


    ### PROPERTIES ###        
    @property
    def end_offset (self) -> bool:
        '''a `bool` indicating if the end date should be offset'''
        return int(self._end_time_str[:2]) >= 24
    
    @property
    def end_time (self) -> time:
        '''the end time of the stop'''
        t = self._end_time_str
        return time(
            hour = 0 if int(t[:2]) >= 24 else int(t[:2]),
            minute = int(t[3:5]),
            seconds = int(t[6:8])
        )
        
    @property
    def _end_time_str (self) -> str:
        '''the end time of the stop as a string'''
        if self.departure_time is None:
            return self.end_pickup_dropoff
        else:
            return self.departure_time
        
    @property
    def start_offset (self) -> bool:
        '''a `bool` indicating if the start date should be offset'''
        return int(self._start_time_str[:2]) >= 24
        
    @property
    def start_time (self) -> time:
        '''the start time of the stop'''
        t = self._start_time_str
        return time(
            hour = 0 if int(t[:2]) >= 24 else int(t[:2]),
            minute = int(t[3:5]),
            seconds = int(t[6:8])
        )
        
    @property
    def _start_time_str (self) -> str:
        '''the start time of the stop as a string'''
        if self.arrival_time is None:
            return self.start_pickup_dropoff
        else:
            return self.arrival_time


STOP_TIME_SCHEMA = d.schema(StopTime)