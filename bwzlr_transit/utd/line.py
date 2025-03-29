from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import desert as d
import marshmallow as m

from .train import Train, TRAIN_SCHEMA


@dataclass
class Line:
    id: str = d.field(m.fields.String())

    name: str = d.field(m.fields.String())
    stations: list[str] = d.field(m.fields.List(m.fields.String()))
    
    inbound: list[Train] = d.field(m.fields.List(m.fields.Nested(TRAIN_SCHEMA)))
    outbound: list[Train] = d.field(m.fields.List(m.fields.Nested(TRAIN_SCHEMA)))


    def __repr__(self) -> str:
        return f'{self.name} ({self.id}): {len(self.inbound)} inbound, {len(self.outbound)} outbound'


    def connects (self, a: str, b: str) -> bool:
        return a in self.stations and b in self.stations
    
    def direction (self, a: str, b: str) -> bool:
        return self.stations.index(b) < self.stations.index(a)
    
    def in_direction (self, direction: bool) -> list[Train]:
        return self.outbound if direction else self.inbound

    def on_date (self, d: date) -> Line:
        return Line(
            self.id, self.name, self.stations, 
            [t for t in self.inbound if min(t.schedule.values()).date() == d],
            [t for t in self.outbound if min(t.schedule.values()).date() == d]
        )


LINE_SCHEMA = d.schema(Line)