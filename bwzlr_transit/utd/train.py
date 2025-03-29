from dataclasses import dataclass
from datetime import datetime

import desert as d
import marshmallow as m


@dataclass
class Train:
    id: str = d.field(m.fields.String())

    schedule: dict[str, datetime] = d.field(m.fields.Dict(keys=m.fields.String(), values=m.fields.DateTime(format='%Y-%m-%d %H:%M:%S')))


TRAIN_SCHEMA = d.schema(Train)