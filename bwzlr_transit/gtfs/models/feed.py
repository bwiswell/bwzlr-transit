from dataclasses import dataclass
from datetime import date
from typing import Optional

import desert as d
import marshmallow as m


@dataclass
class Feed:
    '''
    Contains information about the dataset itself, rather than the services 
    that the dataset describes. In some cases, the publisher of the dataset is 
    a different entity than any of the agencies.
    '''

    # Required fields
    lang: str = d.field(m.fields.String(data_key='feed_lang'))
    '''
    Default language used for the text in this dataset. This setting helps 
    GTFS consumers choose capitalization rules and other language-specific 
    settings for the dataset. The file `translations.txt` can be used if the 
    text needs to be translated into languages other than the default one.

    The default language may be multilingual for datasets with the original 
    text in multiple languages. In such cases, the `feed_lang` field should 
    contain the language code `mul` defined by the norm ISO 639-2, and a 
    translation for each language used in the dataset should be provided in 
    `translations.txt`. If all the original text in the dataset is in the same 
    language, then `mul` should not be used.
    '''
    publisher_name: str = d.field(
        m.fields.String(data_key='feed_publisher_name')
    )
    '''
    Full name of the organization that publishes the dataset. This may be the 
    same as one of the `agency.agency_name` values.
    '''
    publisher_url: str = d.field(
        m.fields.String(data_key='feed_publisher_url')
    )
    '''
    URL of the dataset publishing organization's website. This may be the same 
    as one of the `agency.agency_url` values.
    '''

    # Optional fields
    contact_email: Optional[str] = d.field(
        m.fields.String(data_key='feed_contact_email', missing=None)
    )
    '''
    Email address for communication regarding the GTFS dataset and data 
    publishing practices. `feed_contact_email` is a technical contact 
    for GTFS-consuming applications. Provide customer service contact 
    information through `agency.txt`. It's recommended that at least one of 
    `feed_contact_email` or `feed_contact_url` are provided.
    '''
    contact_url: Optional[str] = d.field(
        m.fields.String(data_key='feed_contact_url', missing=None)
    )
    '''
    URL for contact information, a web-form, support desk, or other tools for 
    communication regarding the GTFS dataset and data publishing practices. 
    `feed_contact_url` is a technical contact for GTFS-consuming applications. 
    Provide customer service contact information through `agency.txt` It's 
    recommended that at least one of `feed_contact_url` or 
    `feed_contact_email` are provided.
    '''
    default_lang: Optional[str] = d.field(
        m.fields.String(data_key='default_lang', missing=None)
    )
    '''
    Defines the language that should be used when the data consumer doesn't 
    know the language of the rider. It will often be `en` (English).
    '''
    end_date: Optional[date] = d.field(
        m.fields.Date(
            data_key='feed_end_date', format='%Y%m%d', missing=None
        )
    )
    '''
    The dataset provides complete and reliable schedule information for 
    service in the period from the beginning of the `feed_start_date` day to 
    the end of the `feed_end_date` day. Both days may be left empty if 
    unavailable. The `feed_end_date` date must not precede the 
    `feed_start_date` date if both are given. It is recommended that dataset 
    providers give schedule data outside this period to advise of likely 
    future service, but dataset consumers should treat it mindful of its 
    non-authoritative status. If `feed_start_date` or `feed_end_date` extend 
    beyond the active calendar dates defined in `calendar.txt` and 
    `calendar_dates.txt`, the dataset is making an explicit assertation that 
    there is no service for dates within the `feed_start_date` or 
    `feed_end_date` range but not included in the active calendar dates.
    '''
    start_date: Optional[date] = d.field(
        m.fields.Date(
            data_key='feed_start_date', format='%Y%m%d', missing=None
        )
    )
    '''
    The dataset provides complete and reliable schedule information for 
    service in the period from the beginning of the `feed_start_date` day to 
    the end of the `feed_end_date` day. Both days may be left empty if 
    unavailable. The `feed_end_date` date must not precede the 
    `feed_start_date` date if both are given. It is recommended that dataset 
    providers give schedule data outside this period to advise of likely 
    future service, but dataset consumers should treat it mindful of its 
    non-authoritative status. If `feed_start_date` or `feed_end_date` extend 
    beyond the active calendar dates defined in `calendar.txt` and 
    `calendar_dates.txt`, the dataset is making an explicit assertation that 
    there is no service for dates within the `feed_start_date` or 
    `feed_end_date` range but not included in the active calendar dates.
    '''
    version: str = d.field(
        m.fields.String(data_key='feed_version', missing=None)
    )
    '''
    String that indicates the current version of their GTFS dataset. 
    GTFS-consuming applications can display this value to help dataset 
    publishers determine whether the latest dataset has been incorporated.
    '''


FEED_SCHEMA = d.schema(Feed)