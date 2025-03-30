from typing import Callable, TypeVar

import marshmallow as m
import pandas as pd


T = TypeVar('T', object, object)

KeyGetter = Callable[[T], str]



def load_list (path: str, schema: m.Schema) -> list[T]:
    '''
    Reads a CSV file and returns a list of deserialized records.

    Parameters:
        path (str):
            the path of the CSV file to load data from
        schema (marshmallow.Schema):
            the Schema for the records in the CSV file

    Returns:
        records (list[T]):
            a list of deserialized records
    '''
    data: list[str]
    with open(path, 'r') as file:
        data = file.readlines()

    header = data[0].rstrip().split(',')
    data = [l.rstrip().split(',') for l in data[1:]]

    return [
        schema.load({ 
            head: val 
            for head, val in zip(header, values) 
        }) for values in data
    ]

    
def load_table (
            path: str, 
            schema: m.Schema, 
            key_fn: KeyGetter
        ) -> dict[str, T]:
    '''
    Reads a CSV file and returns a dict mapping `str` IDs to deserialized 
    records.

    Parameters:
        path (str):
            the path of the CSV file to load data from
        schema (marshmallow.Schema):
            the Schema for the records in the CSV file
        key_fn (KeyGetter):
            a function that extracts a key from a record

    Returns:
        data (dict[str, T]):
            a dict mapping `str` keys to deserialized records
    '''
    values = load_list(path, schema)

    return { 
        key_fn(value): value 
        for value in values 
    }