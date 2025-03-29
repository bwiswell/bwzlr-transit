from dataclasses import dataclass
from datetime import date

import desert as d
import marshmallow as m


@dataclass
class Feed:
    end: date = d.field(m.fields.Date(data_key='feed_end_date', format='%Y%m%d'))
    start: date = d.field(m.fields.Date(data_key='feed_start_date', format='%Y%m%d'))
    
    lang: str = d.field(m.fields.String(data_key='feed_lang'))
    publisher_name: str = d.field(m.fields.String(data_key='feed_publisher_name'))
    publisher_url: str = d.field(m.fields.String(data_key='feed_publisher_url'))
    version: str = d.field(m.fields.String(data_key='feed_version'))


FEED_SCHEMA = d.schema(Feed)