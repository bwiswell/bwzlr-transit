from dataclasses import dataclass
from typing import Optional

import desert as d
import marshmallow as m


@dataclass
class Agency:
    '''
    A GTFS dataclass model for records found in `agency.txt`. Identifies a 
    transit agency.

    Attributes:
        id (str):
            the unique ID of the transit agency
        email (Optional[str]):
            the customer service email of the transit agency
        fare_url (Optional[str]):
            the URL of a fare or ticket website for the transit agency
        lang (str):
            the primary language used by the transit agency
        name (str):
            the name of the transit agency
        phone (str):
            the voice telephone number for the transit agency
        timezone (str):
            the timezone where the transit agency is located
        url (str):
            the URL of the transit agency
    '''
    
    ### ATTRIBUTES ###
    # Model ID
    id: str = d.field(m.fields.String(data_key='agency_id', missing=''))
    '''the unique ID of the transit agency'''
    
    # Required fields
    name: str = d.field(m.fields.String(data_key='agency_name'))
    '''the name of the transit agency'''
    timezone: str = d.field(m.fields.String(data_key='agency_timezone'))
    '''the timezone where the transit agency is located'''
    url: str = d.field(m.fields.String(data_key='agency_url'))
    '''the URL of the transit agency'''

    # Optional fields
    email: Optional[str] = d.field(
        m.fields.String(data_key='agency_email', missing=None)
    )
    '''the customer service email of the transit agency'''
    fare_url: Optional[str] = d.field(
        m.fields.String(data_key='agency_fare_url', missing=None)
    )
    '''the URL of a fare or ticket website for the transit agency'''
    lang: Optional[str] = d.field(
        m.fields.String(data_key='agency_lang', missing=None)
    )
    '''the primary language used by the transit agency'''
    phone: Optional[str] = d.field(
        m.fields.String(data_key='agency_phone', missing=None)
    )
    '''the voice telephone number for the transit agency'''


AGENCY_SCHEMA = d.schema(Agency)