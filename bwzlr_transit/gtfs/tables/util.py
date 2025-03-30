from typing import Callable, TypeVar

import marshmallow as m
import pandas as pd


T = TypeVar('T', object, object)

KeyGetter = Callable[[T], str]

    
def load_table (
            path: str, 
            schema: m.Schema, 
            key_fn: KeyGetter
        ) -> dict[str, T]:
    '''
    Reads the contents of a table in CSV format and deserializes its contents.

    Parameters:
        path (str):
            the path of the CSV file to load data from
        schema (marshmallow.Schema):
            the Schema for the table's records
        key_fn (KeyGetter):
            a function that extracts a key from a record

    Returns:
        data (dict[str, T]):
            a dictionary mapping `str` keys to deserialized record objects
    '''
    
    df = pd.read_csv(path, dtype=str).fillna('')
    json = df.to_dict(orient='records')

    values = []
    for rec in json:
        values.append(schema.load(rec))

    return { 
        key_fn(value): value 
        for value in values 
    }