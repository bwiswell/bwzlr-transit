from dataclasses import dataclass

import desert as d
import marshmallow as m


@dataclass
class Route:
    id: str = d.field(m.fields.String(data_key='route_id'))
    
    agency_id: str = d.field(m.fields.String())
    color: str = d.field(m.fields.String(data_key='route_color'))
    desc: str = d.field(m.fields.String(data_key='route_desc'))
    name: str = d.field(m.fields.String(data_key='route_long_name'))
    short_name: str = d.field(m.fields.String(data_key='route_short_name'))
    text_color: str = d.field(m.fields.String(data_key='route_text_color'))
    type: int = d.field(m.fields.Integer(data_key='route_type'))
    url: str = d.field(m.fields.String(data_key='route_url'))


ROUTE_SCHEMA = d.schema(Route)