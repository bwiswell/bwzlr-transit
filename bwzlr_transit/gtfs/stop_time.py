from dataclasses import dataclass
from datetime import time

import desert as d
import marshmallow as m


@dataclass
class StopTime:
    stop_id: str = d.field(m.fields.String())
    trip_id: str = d.field(m.fields.String())

    arrival: time = d.field(
        m.fields.Function(
            data_key='arrival_time', 
            deserialize=lambda at: time(int(at[:2]) if int(at[:2]) < 24 else 0, int(at[3:5]), int(at[6:8]))
        )
    )
    departure: time = d.field(
        m.fields.Function(
            data_key='departure_time', 
            deserialize=lambda at: time(int(at[:2]) if int(at[:2]) < 24 else 0, int(at[3:5]), int(at[6:8]))
        )
    )
    dropoff_type: int = d.field(m.fields.Integer(data_key='drop_off_type'))
    pickup_type: int = d.field(m.fields.Integer())
    sequence: int = d.field(m.fields.Integer(data_key='stop_sequence'))


STOPTIME_SCHEMA = d.schema(StopTime)