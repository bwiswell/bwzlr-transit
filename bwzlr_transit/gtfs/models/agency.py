from dataclasses import dataclass
from typing import Optional

import desert as d
import marshmallow as m


@dataclass
class Agency:
    '''
    Identifies a transit brand which is often synonymous with a transit agency. 
    Note that in some cases, such as when a single agency operates multiple 
    separate services, agencies and brands are distinct. This module uses the 
    term "agency" in place of "brand". A dataset may contain data from multiple
    agencies.
    '''
    
    # Model ID
    id: str = d.field(m.fields.String(data_key='agency_id'))
    '''Unique identifier of the transit agency.'''
    
    # Required fields
    name: str = d.field(m.fields.String(data_key='agency_name'))
    '''Full name of the transit agency.'''
    timezone: str = d.field(m.fields.String(data_key='agency_timezone'))
    '''
    Timezone where the transit agency is located. If multiple agencies are 
    specified in the dataset, each must have the same `agency_timezone`.
    '''
    url: str = d.field(m.fields.String(data_key='agency_url'))
    '''URL of the transit agency.'''

    # Optional fields
    email: Optional[str] = d.field(
        m.fields.String(data_key='agency_email', missing=None)
    )
    '''
    Email address actively monitored by the agency's customer service 
    department. This email address should be a direct contact point where 
    transit riders can reach a customer service representative at the agency.
    '''
    fare_url: Optional[str] = d.field(
        m.fields.String(data_key='agency_fare_url', missing=None)
    )
    '''
    URL of a web page where a rider can purchase tickets or other fare 
    instruments for that agency, or a web page containing information about 
    that agency's fares.
    '''
    lang: Optional[str] = d.field(
        m.fields.String(data_key='agency_lang', missing=None)
    )
    '''
    Primary language used by this transit agency. Should be provided to help 
    GTFS consumers choose capitalization rules and other language-specific 
    settings for the dataset.
    '''
    phone: Optional[str] = d.field(
        m.fields.String(data_key='agency_phone', missing=None)
    )
    '''
    A voice telephone number for the specified agency. This field is a string 
    value that presents the telephone number as typical for the agency's 
    service area. It may contain punctuation marks to group the digits of the 
    number. Dialable text (for example, TriMet's "503-238-RIDE") is permitted,
    but the field must not contain any other descriptive text.
    '''


AGENCY_SCEMA = d.schema(Agency)