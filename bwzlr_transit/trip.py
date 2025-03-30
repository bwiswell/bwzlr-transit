from dataclasses import dataclass

import desert as d
import marshmallow as m


@dataclass
class Trip:
    id: str = d.field(m.fields.String(data_key='trip_id'))

    block_id: str = d.field(m.fields.String())
    direction_id: int = d.field(m.fields.Integer())
    route_id: str = d.field(m.fields.String())
    service_id: str = d.field(m.fields.String())
    shape_id: str = d.field(m.fields.String())

    headsign: str = d.field(m.fields.String(data_key='trip_headsign'))
    name: str = d.field(m.fields.String(data_key='trip_short_name'))



TRIP_SCHEMA = d.schema(Trip)