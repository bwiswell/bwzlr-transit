from dataclasses import dataclass

import desert as d
import marshmallow as m


@dataclass
class Stop:
    id: str = d.field(m.fields.String(data_key='stop_id'))
    zone_id: str = d.field(m.fields.String())

    desc: str = d.field(m.fields.String(data_key='stop_desc'))
    name: str = d.field(m.fields.String(data_key='stop_name'))
    lat: float = d.field(m.fields.Float(data_key='stop_lat'))
    lon: float = d.field(m.fields.Float(data_key='stop_lon'))
    url: str = d.field(m.fields.String(data_key='stop_url'))


STOP_SCHEMA = d.schema(Stop)