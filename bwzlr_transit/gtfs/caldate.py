from dataclasses import dataclass
from datetime import date as pydate

import desert as d
import marshmallow as m


@dataclass
class CalDate:
    service_id: str = d.field(m.fields.String())
    
    date: pydate = d.field(m.fields.Date(format='%Y%m%d'))
    exception: int = d.field(m.fields.Integer(data_key='exception_type'))


CALDATE_SCHEMA = d.schema(CalDate)