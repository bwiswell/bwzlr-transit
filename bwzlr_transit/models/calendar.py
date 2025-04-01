from dataclasses import dataclass
from datetime import date

import desert as d
import marshmallow as m


@dataclass
class Calendar:
    '''
    A GTFS dataclass model for records found in `calendar.txt`. Defines a \
    default schedule for a transit service.

    Attributes:
        service_id (str):
            the unique ID of the transit service the schedule is defined for
        end (date):
            the end date of the service schedule
        friday (bool):
            a `bool` indicating if the service is active on Fridays
        monday (bool):
            a `bool` indicating if the service is active on Mondays
        saturday (bool):
            a `bool` indicating if the service is active on Saturdays
        start (date):
            the start date of the service schedule
        sunday (bool):
            a `bool` indicating if the service is active on Sundays
        thursday (bool):
            a `bool` indicating if the service is active on Thursdays
        saturday (bool):
            a `bool` indicating if the service is active on Saturdays
        schedule (list[bool]):
            a list of `bool` indicating if service is available on a given day \
            when indexed by weekday
        sunday (bool):
            a `bool` indicating if the service is active on Sundays
    '''
    
    ### ATTRIBUTES ###
    # Foreign IDs
    service_id: str = d.field(m.fields.String(data_key='service_id'))
    '''the unique ID of the transit service the schedule is defined for'''

    # Required fields
    end: date = d.field(m.fields.Date(data_key='end_date', format='%Y%m%d'))
    '''the end date of the service schedule'''
    friday: bool = d.field(m.fields.Boolean(data_key='friday'))
    '''a `bool` indicating if the service is active on Fridays'''
    monday: bool = d.field(m.fields.Boolean(data_key='monday'))
    '''a `bool` indicating if the service is active on Mondays'''
    saturday: bool = d.field(m.fields.Boolean(data_key='saturday'))
    '''a `bool` indicating if the service is active on Saturdays'''
    start: date = d.field(m.fields.Date(data_key='start_date', format='%Y%m%d'))
    '''the start date of the service schedule'''
    sunday: bool = d.field(m.fields.Boolean(data_key='sunday'))
    '''a `bool` indicating if the service is active on Sundays'''
    thursday: bool = d.field(m.fields.Boolean(data_key='thursday'))
    '''a `bool` indicating if the service is active on Thursdays'''
    tuesday: bool = d.field(m.fields.Boolean(data_key='tuesday'))
    '''a `bool` indicating if the service is active on Tuesdays'''
    wednesday: bool = d.field(m.fields.Boolean(data_key='wednesday'))
    '''a `bool` indicating if the service is active on Wednesdays'''

    @property
    def schedule (self) -> list[bool]:
        '''
        a list of `bool` indicating if service is available on a given day \
        when indexed by weekday
        '''
        return [
            self.monday,
            self.tuesday,
            self.wednesday,
            self.thursday,
            self.friday,
            self.saturday,
            self.sunday
        ]


CALENDAR_SCHEMA = d.schema(Calendar)