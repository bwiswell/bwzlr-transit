from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Optional

import desert as d
import marshmallow as m

from .stop_time import StopTime, STOP_TIME_SCHEMA


@dataclass
class Timetable:
    '''
    Serializable dataclass table mapping `str` stop IDs to `StopTime` records.

    Attributes:
        data (dict[str, StopTime]):
            a `dict` mapping `str` stop IDs to `StopTime` records
        end (StopTime)
            the last `StopTime` record in the table chronologically
        start (StopTime)
            the first `StopTime` record in the table chronologically
        stop_ids (list[str]):
            a `list` of all `str` stop IDs in the `Timetable` table
        stops (list[StopTime]):
            a `list` of all `StopTime` records in the `Timetable` table
    '''

    ### ATTRIBUTES ###
    data: dict[str, StopTime] = d.field(
        m.fields.Function(
            deserialize=lambda data: { 
                id: STOP_TIME_SCHEMA.load(d) for id, d in data.items() 
            },
            serialize=lambda data: { 
                d.stop_id: STOP_TIME_SCHEMA.dump(d) for d in data.data.values() 
            }
        )
    )
    '''a `dict` mapping `str` stop IDs to `StopTime` records'''


    ### CLASS METHODS ###
    @classmethod
    def from_gtfs (cls, stops: list[StopTime]) -> Timetable:
        '''
        Returns an `Timetable` populated from `stops`.

        Parameters:
            stops (list[StopTime]):
                a `list` of `StopTime` records to put in the `Timetable`

        Returns:
            timetable (Timetable):
                an `Timetable` populated from `stops`
        '''
        return Timetable({ s.stop_id: s for s in stops })


    ### PROPERTIES ###    
    @property
    def end (self) -> StopTime:
        '''the last `StopTime` record in the table chronologically'''
        return self.stops[-1]
    
    @property
    def start (self) -> StopTime:
        '''the first `StopTime` record in the table chronologically'''
        return self.stops[0]
    
    @property
    def stop_ids (self) -> list[str]:
        '''a `list` of all `str` stop IDs in the `Timetable` table'''
        return list(self.data.keys())
     
    @property
    def stops (self) -> list[StopTime]:
        '''an ordered list of all `Stop` records in the table'''
        return sorted(
            list(self.data.values()), 
            key=lambda st: st.index
        )
    

    ### MAGIC METHODS ###
    def __getitem__ (self, id: str) -> Optional[StopTime]:
        '''
        Returns the `StopTime` record associated with the `id` if it exists,
        otherwise returns `None`.
        
        Parameters:
            id (str):
                the `str` id associated with the `StopTime` record to retrieve

        Returns:
            record (Optional[StopTime]):
                the `StopTime` record associated with `id` if it exists, 
                otherwise `None`
        '''
        return self.data.get(id, None)
    

    ### METHODS ###
    def between (self, start: time, end: time) -> bool:
        return self.start <= end and self.end >= start

    def connects (self, stop_a_id: str, stop_b_id: str) -> bool:
        '''
        Returns a `bool` indicating if the `Timetable` contains chronologically
        ordered entries for both `stop_a_id` and `stop_b_id`.

        Parameters:
            stop_a_id (str):
                the unique ID associated with the first stop
            stop_b_id (str):
                the unique ID associated with the second stop

        Returns:
            a `bool` indicating if the `Timetable` contains chronologically
            ordered entries for both `stop_a_id` and `stop_b_id`
        '''
        return stop_a_id in self.data and stop_b_id in self.data and \
            self[stop_a_id].index < self[stop_b_id].index
        
    @property
    def location (self) -> tuple[Optional[StopTime], Optional[StopTime]]:
        t = datetime.now().time()
        if (self.start.start_time <= t and t <= self.end.end_time) or \
                (self.start.start_time <= t and self.end.end_offset) or \
                (self.end.end_offset and t <= self.end.end_time):
            stops = self.stops
            for i in range(len(stops - 1)):
                a, b = stops[i], stops[i+1]
                if (a.start_time <= t and t <= b.end_time) or \
                        (a.start_time <= t and b.end_offset) or \
                        (b.end_offset and t <= b.end_time):
                    return a, b
        else:
            tm = t.hour * 60 + t.minute
            sm = self.start.start_time.hour * 60 + self.start.start_time.minute
            em = self.end.end_time.hour * 60 + self.end.end_time.minute
            tts = abs(tm - sm)
            tte = abs(tm - em)
            if tts < tte:
                return None, self.start
            else:
                return self.end, None
            
    

TIMETABLE_SCHEMA = d.schema(Timetable)