from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import desert as d
import marshmallow as m


@dataclass(frozen=True)
class DateRange:
    '''
    A dataclass model for storing a weekly schedule for an inclusive date
    range.

    Attributes:
        end (date):
            the end `date` of the range
        schedule (list[bool]):
            a `list` of `bool` indicating if service is active when indexed
            by weekday
        start (date):
            the start `date` of the range
    '''

    ### ATTRIBUTES ###
    end: date = d.field(m.fields.Date())
    '''the end `date` of the range'''
    schedule: list[bool] = d.field(m.fields.List(m.fields.Boolean()))
    '''
    a `list` of `bool` indicating if service is active when indexed by weekday
    '''
    start: date = d.field(m.fields.Date())
    '''the start `date` of the range'''


DATE_RANGE_SCHEMA = d.schema(DateRange)