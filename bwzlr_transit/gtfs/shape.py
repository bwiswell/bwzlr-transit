from dataclasses import dataclass

import desert as d
import marshmallow as m


@dataclass
class Shape:
    id: str = d.field(m.fields.String(data_key='shape_id'))

    dist: float = d.field(m.fields.Float(data_key='shape_dist_traveled'))
    lat: float = d.field(m.fields.Float(data_key='shape_pt_lat'))
    lon: float = d.field(m.fields.Float(data_key='shape_pt_lon'))
    sequence: int = d.field(m.fields.Integer(data_key='shape_pt_sequence'))


SHAPE_SCHEMA = d.schema(Shape)