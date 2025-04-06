from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import os
from typing import Optional

import desert as d
import marshmallow as m

from ..util import load_list


@dataclass
class Feed:
    '''
    A GTFS dataclass model for records found in `feed_info.txt`. Describes a 
    GTFS dataset and publisher.

    Attributes:
        contact_email (Optional[str]):
            the email address for communication regarding the GTFS dataset
        contact_url (Optional[str]):
            the URL for information regarding the GTFS dataset
        default_lang (Optional[str]):
            the language to use when the rider's language is unknown
        end_date (Optional[date]):
            the end date of the information provided in the GTFS dataset
        lang (str):
            the default language used for the text in this dataset
        publisher_name (str):
            the name of the organization that publishes the dataset
        publisher_url (str):
            the url of the dataset publishing organization's website
        start_date (Optional[date]):
            the start date of the information provided in the GTFS dataset
        version (Optional[str]):
            the current version of the GTFS dataset
    '''

    ### ATTRIBUTES ###
    # Required fields
    lang: str = d.field(m.fields.String(data_key='feed_lang'))
    '''the default language used for the text in this dataset'''
    publisher_name: str = d.field(
        m.fields.String(data_key='feed_publisher_name')
    )
    '''the name of the organization that publishes the dataset'''
    publisher_url: str = d.field(
        m.fields.String(data_key='feed_publisher_url')
    )
    '''the url of the dataset publishing organization's website'''

    # Optional fields
    contact_email: Optional[str] = d.field(
        m.fields.String(data_key='feed_contact_email', missing=None)
    )
    '''the email address for communication regarding the GTFS dataset'''
    contact_url: Optional[str] = d.field(
        m.fields.String(data_key='feed_contact_url', missing=None)
    )
    '''the URL for information regarding the GTFS dataset'''
    default_lang: Optional[str] = d.field(
        m.fields.String(data_key='default_lang', missing=None)
    )
    '''the language to use when the rider's language is unknown'''
    end_date: Optional[date] = d.field(
        m.fields.Date(
            data_key='feed_end_date', format='%Y%m%d', missing=None
        )
    )
    '''the end date of the information provided in the GTFS dataset'''
    start_date: Optional[date] = d.field(
        m.fields.Date(
            data_key='feed_start_date', format='%Y%m%d', missing=None
        )
    )
    '''the start date of the information provided in the GTFS dataset'''
    version: str = d.field(
        m.fields.String(data_key='feed_version', missing=None)
    )
    '''the current version of the GTFS dataset'''


    ### CLASS METHODS ###
    @classmethod
    def from_gtfs (self, path: str) -> Feed:
        '''
        Returns a `Feed` record populated from the GTFS data at `path`.

        Parameters:
            path (str):
                the path to the GTFS dataset

        Returns:
            feed (Feed):
                a `Feed` record populated from the GTFS data at `path`
        '''
        return load_list(
            os.path.join(path, 'feed_info.txt'), 
            FEED_SCHEMA
        )[0]


FEED_SCHEMA = d.schema(Feed)