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
    Used in conjunction with `Calendar` to define exceptions to the default 
    service patterns defined in `calendar.txt`. If service is generally 
    regular, with a few changes on explicit dates (for instance, to accomodate 
    special event services, or a school schedule), this is a good approach. In 
    this case `calendar_dates.service_id` is a foreign ID referencing 
    `calendar.service_id`. Alternatively, omit `calendar.txt` and specify each 
    date of service in `calendar_dates.txt`. This allows for considerable 
    service variation and accommodates service without normal weekly 
    schedules. In this case `service_id` is an ID.
    '''

    # Foreign IDs
    service_id: str = d.field(m.fields.String(data_key='service_id'))
    '''
    Identifies a set of dates when a service exception occurs for one or more 
    routes. Each (`service_id`, `date`) pair may only appear once in 
    `calendar_dates.txt` if using `calendar.txt` and `calendar_dates.txt` in 
    conjunction. If a `service_id` value appears in both `calendar.txt` and 
    `calendar_dates.txt`, the information in `calendar_dates.txt` modifies the 
    service information specified in `calendar.txt`.
    '''
    
    # Required fields
    date: pydate = d.field(m.fields.Date(data_key='date', format='%Y%m%d'))
    '''Date when service exception occurs.'''
    exception: ExceptionType = d.field(
        m.fields.Enum(ExceptionType, data_key='exception_type', by_value=True)
    )
    '''
    Indicates whether service is avilable on the date specified in the date 
    field. Valid options are:
    
    `1` - Service has been added for the specified date.\n    
    `2` - Service has been removed for the specified date.
    '''


CALENDAR_DATE_SCHEMA = d.schema(CalendarDate)