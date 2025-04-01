from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..gtfs import (
    Accessibility, 
    BikesAllowed, 
    StopTime,
    Trip as GTFSTrip
)

from .timetable import Timetable


@dataclass
class Trip:
    '''
    A dataclass model that defines a single trip.

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
        timetable (Timetable):
            the `Timetable` for the trip
    '''

    ### ATTRIBUTES ###
    # Model ID
    id: str
    '''the unique ID of the trip'''

    # Foreign IDs
    block_id: Optional[str]
    '''the unique ID of the block the trip belongs to'''
    route_id: str
    '''the unique ID of the route the trip belongs to'''
    service_id: str
    '''the unique ID of the service the trip belongs to'''
    shape_id: Optional[str]
    '''the unique ID of the shape for the trip'''

    # Required fields
    accessibility: Accessibility
    '''the `Accessibility` of the trip'''
    bikes: BikesAllowed
    '''the `BikesAllowed` of the trip'''
    timetable: Timetable
    '''the `Timetable` for the trip'''

    # Optional fields
    direction: Optional[bool]
    '''the direction of the trip'''
    headsign: Optional[str]
    '''the headsign to display for the trip'''
    short_name: Optional[str]
    '''a short name for the trip'''


    ### CLASS METHODS ###
    @classmethod
    def from_gtfs (
                cls,
                trip: GTFSTrip,
                stop_times: list[StopTime]
            ) -> Trip:
        '''
        Convert a `gtfs.Trip` into a `helpers.Trip` with timetable data using  
        the provided `StopTime` records.

        Parameters:
            trip (gtfs.Trip):
                the `gtfs.Trip` to convert
            stop_times (list[StopTime]):
                a list of all `StopTime` records in the GTFS dataset

        Returns:
            trip (helpers.Trip):
                a dataclass model that defines a single trip
        '''
        stops = [st for st in stop_times if st.trip_id == trip.id]
        return Trip(
            id=trip.id,
            block_id=trip.block_id,
            route_id=trip.route_id,
            service_id=trip.service_id,
            shape_id=trip.shape_id,
            accessibility=trip.accessibility,
            bikes=trip.bikes,
            timetable=Timetable({ s.stop_id: s for s in stops }),
            direction=trip.direction,
            headsign=trip.headsign,
            short_name=trip.short_name
        )