from dataclasses import dataclass
from datetime import date

import desert as d
import marshmallow as m


@dataclass
class Schedule:
    service_id: str = d.field(m.fields.String())

    end: date = d.field(m.fields.Date(data_key='end_date', format='%Y%m%d'))
    start: date = d.field(m.fields.Date(data_key='start_date', format='%Y%m%d'))

    monday: bool = d.field(m.fields.Boolean())
    tuesday: bool = d.field(m.fields.Boolean())
    wednesday: bool = d.field(m.fields.Boolean())
    thursday: bool = d.field(m.fields.Boolean())
    friday: bool = d.field(m.fields.Boolean())
    saturday: bool = d.field(m.fields.Boolean())
    sunday: bool = d.field(m.fields.Boolean())

    @property
    def schedule (self) -> list[bool]:
        return [
            self.monday,
            self.tuesday,
            self.wednesday,
            self.thursday,
            self.friday,
            self.saturday,
            self.sunday
        ]


SCHEDULE_SCHEMA = d.schema(Schedule)