from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
import json
from typing import Generator

import desert as d
import marshmallow as m

from ..gtfs import GTFS, StopTime, Trip

from .line import Line, LINE_SCHEMA
from .station import Station, STATION_SCHEMA
from .train import Train


@dataclass
class UTD:

    agency_id: str = d.field(m.fields.String())
    lines: dict[str, Line] = d.field(m.fields.Dict(keys=m.fields.String(), values=m.fields.Nested(LINE_SCHEMA)))
    stations: dict[str, Station] = d.field(m.fields.Dict(keys=m.fields.String(), values=m.fields.Nested(STATION_SCHEMA)))


    @classmethod
    def from_gtfs (cls, gtfs: GTFS) -> UTD:
        agency_id = gtfs.agency.id
        stations = { s.id: Station(s.id, s.name) for s in gtfs.stops }

        def _service_dates (service_id: str) -> Generator[date, None, None]:
            is_extra = (service_id in gtfs.dates) and (gtfs.dates[service_id].exception == 1)
            if is_extra:
                for sid, cd in gtfs.dates.items():
                    if sid == service_id:
                        yield cd.date
            else:
                exceptions = [cd.date for sid, cd in gtfs.dates.items() if sid == service_id]
                regular = gtfs.calendar[service_id].schedule
                curr = gtfs.calendar[service_id].start
                day_td = timedelta(1)
                while curr <= gtfs.calendar[service_id].end:
                    if (not curr in exceptions) and regular[curr.weekday()]:
                        yield curr
                    curr += day_td

        def _load_line (id: str) -> Line:
            inbound: list[Train] = []
            outbound: list[Train] = []

            route = gtfs.routes[id]
            trips = [t for t in gtfs.trips if t.route_id == id]
            i_trips = [t for t in trips if t.direction_id == 0]
            o_trips = [t for t in trips if t.direction_id == 1]

            i_trip_its = [[st for st in gtfs.stop_times if st.trip_id == t.id] for t in i_trips]
            o_trip_its = [[st for st in gtfs.stop_times if st.trip_id == t.id] for t in o_trips]

            def st_key (st: StopTime) -> int:
                hi = st.departure.hour if st.departure.hour > 0 else 24
                mi = st.departure.minute
                return hi * 60 + mi

            for i_trip_it in i_trip_its: i_trip_it.sort(key=st_key)
            for o_trip_it in o_trip_its: o_trip_it.sort(key=st_key)

            i_trip_lens = [len(i_trip_it) for i_trip_it in i_trip_its]
            test_i = i_trip_its[i_trip_lens.index(max(i_trip_lens))]
            l_stations = [s.stop_id for s in test_i]

            def add_trains (trains: list[Train], trips: list[Trip], its: list[list[StopTime]]):
                for i, trip in enumerate(trips):
                    for s_date in _service_dates(trip.service_id):
                        trains.append(
                            Train(
                                trip.id,
                                {
                                    s.stop_id: datetime.combine(
                                        s_date if s.departure.hour > 0 else s_date + timedelta(1),
                                        s.departure
                                    ) for s in its[i]
                                }
                            )
                        )
            
            add_trains(inbound, i_trips, i_trip_its)
            add_trains(outbound, o_trips, o_trip_its)

            return Line(id, route.name, l_stations, inbound, outbound)
        
        lines = { id: _load_line(id) for id in gtfs.routes }

        return UTD(agency_id, lines, stations)
    

    @classmethod
    def load (cls, path: str) -> UTD:
        with open(path, 'r') as file:
            data = json.load(file)
        schema = d.schema(cls)
        return schema.load(data)


    def connecting (self, a: str, b: str) -> list[Train]:
        lines = [l for l in self.lines.values() if l.connects(a, b)]
        trains: list[Train] = []
        for line in lines:
            direction = line.direction(a, b)
            trains.extend([
                t for t in line.in_direction(direction)
                if a in t.schedule and b in t.schedule
            ])
        return trains
    
    def on_date (self, d: date) -> UTD:
        return UTD(
            self.agency_id,
            { id: line.on_date(d) for id, line in self.lines.items() },
            self.stations
        )

    def save (self, path: str):
        schema = d.schema(UTD)
        data = schema.dump(self)
        with open(path, 'w') as file:
            json.dump(data, file)
    
    def station (self, name: str) -> Station:
        return [s for s in self.stations.values() if s.name == name][0]