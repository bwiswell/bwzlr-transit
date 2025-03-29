from dataclasses import dataclass

import desert as d
import marshmallow as m


@dataclass
class Agency:
    id: str = d.field(m.fields.String(data_key='agency_id'))
    
    email: str = d.field(m.fields.String(data_key='agency_email'))
    lang: str = d.field(m.fields.String(data_key='agency_lang'))
    name: str = d.field(m.fields.String(data_key='agency_name'))
    timezone: str = d.field(m.fields.String(data_key='agency_timezone'))
    url: str = d.field(m.fields.String(data_key='agency_url'))


AGENCY_SCEMA = d.schema(Agency)