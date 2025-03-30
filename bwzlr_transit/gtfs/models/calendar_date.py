from dataclasses import dataclass
from datetime import date as pydate
from enum import Enum

import desert as d
import marshmallow as m


class ExceptionType(Enum):
    ADD = 1
    REMOVE = 2


@dataclass
class CalendarDate:
    '''
    A GTFS dataclass model for records found in `calendar_dates.txt`. 
    Defines an exception to the service patterns defined in `calendar.txt`.

    Attributes:
        date (date): the date when the service exception occurs
        exception (ExceptionType): the type of service exception specified
        service_id (str): the ID of the service the calendar date modifies
    '''

    # Foreign IDs
    service_id: str = d.field(m.fields.String(data_key='service_id'))
    '''the ID of the service the calendar date modifies'''
    
    # Required fields
    date: pydate = d.field(m.fields.Date(data_key='date', format='%Y%m%d'))
    '''the date when the service exception occurs'''
    exception: ExceptionType = d.field(
        m.fields.Enum(ExceptionType, data_key='exception_type', by_value=True)
    )
    '''
    The type of service exception specified. Indicates whether service is 
    avilable on `date`. Valid options are:
    
    `1` - Service has been added for the specified date.\n    
    `2` - Service has been removed for the specified date.
    '''


CALENDAR_DATE_SCHEMA = d.schema(CalendarDate)