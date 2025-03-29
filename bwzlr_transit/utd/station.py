from dataclasses import dataclass

import desert as d
import marshmallow as m


@dataclass
class Station:
    id: str = d.field(m.fields.String())

    name: str = d.field(m.fields.String())


STATION_SCHEMA = d.schema(Station)