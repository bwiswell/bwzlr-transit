from __future__ import annotations

from dataclasses import dataclass
from datetime import date as pydate

from ..gtfs import Calendar, CalendarDate, ExceptionType


@dataclass
class Schedule:
    '''
    A dataclass model that defines a schedule for a transit service.

    Attributes:
        additions (list[date]): 
            a list of dates on which additional service is offered
        calendars (list[Calendar]):
            a list of `Calendar` records associated with the transit service
        end (date):
            the end date of the transit schedule
        exceptions (list[date]): 
            a list of dates on which service is suspended
        start (date):
            the start date of the transit schedule
    '''

    ### ATTRIBUTES ###
    # Required fields
    additions: list[pydate]
    '''a list of dates on which additional service is offered'''
    calendars: list[Calendar]
    '''a list of `Calendar` records associated with the service'''
    exceptions: list[pydate]
    '''a list of dates on which service is suspended'''


    ### CLASS METHODS ###
    @classmethod
    def from_gtfs (
                cls,
                calendars: list[Calendar],
                dates: list[CalendarDate]
            ) -> Schedule:
        '''
        Returns a `Schedule` created from the given `Calendar` and 
        `CalendarDate` records.

        All `Calendar` and `CalendarDate` values should be for the same 
        transit service.

        Parameters:
            calendars (list[Calendar]):
                a list of `Calendar` records associated with a transit service
            dates (list[CalendarDate]):
                a list of `CalendarDate` records associated with a transit \
                service

        Returns:
            schedule (Schedule):
                a dataclass model that defines a schedule for a transit service
        '''
        additions = [d for d in dates if d.exception == ExceptionType.ADD]
        exceptions = [d for d in dates if d.exception == ExceptionType.REMOVE]
        return Schedule(additions, exceptions, calendars)


    ### PROPERTIES ###
    @property
    def end (self) -> pydate:
        '''the end date of the transit schedule'''
        return max([c.end for c in self.calendars])
    
    @property
    def start (self) -> pydate:
        '''the start date of the transit schedule'''
        return min([c.start for c in self.calendars])


    ### METHODS ###
    def active (self, date: pydate) -> bool:
        '''
        Returns a `bool` indicating if the service is active on `date`.

        Returns `False` if `date` is outside of the GTFS dataset's 
        `feed_start_date` and `feed_end_date`.

        Parameters:
            date (date):
                the date to check for active service

        Returns:
            active (bool):
                a `bool` indicating if the service is active on `date`
        '''
        if date in self.additions: return True
        if date in self.exceptions: return False
        for cal in self.calendars:
            if cal.start <= date and date <= cal.end:
                return cal.schedule[date.weekday()]
        return False