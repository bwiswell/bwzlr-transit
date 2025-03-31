import json
import os
import shutil
from typing import Optional
from urllib import request
import zipfile

from .gtfs import GTFS, GTFS_SCHEMA
from .models import Feed
from .tables import Agencies, Routes, Schedules, Trips


def save_minified_gtfs (gtfs: GTFS, path: str):
    print('saving minified GTFS data...')
    data = GTFS_SCHEMA.dump(gtfs)
    with open(path, 'w') as file:
        json.dump(data, file)

def load_gtfs (
            name: str, 
            path: str,
            minified_path: Optional[str] = None
        ) -> GTFS:
    print('loading GTFS data...')
    g = GTFS(
        name=name, 
        feed=Feed.from_gtfs(path),
        agencies=Agencies.from_gtfs(path), 
        routes=Routes.from_gtfs(path), 
        schedules=Schedules.from_gtfs(path), 
        trips=Trips.from_gtfs(path)
    )
    if minified_path: save_minified_gtfs(g, minified_path)
    return g

def load_minified_gtfs (path: str) -> GTFS:
    print('loading minified GTFS data...')
    data = {}
    with open(path, 'r') as file:
        data = json.load(file)
    return GTFS_SCHEMA.load(data)

def fetch_gtfs (
            name: str,
            uri: str,
            sub: Optional[str] = None,
            minified_path: Optional[str] = None
        ) -> GTFS:
    print(f'fetching GTFS data from {uri}...')
    tmp_dir = os.path.join(
        os.path.realpath(os.path.dirname(__file__)),
        'tmp'
    )
    os.mkdir(tmp_dir)

    zip_path = os.path.join(tmp_dir, f'{name}.zip')
    request.urlretrieve(uri, zip_path)
    with zipfile.ZipFile(zip_path) as zip:
        zip.extractall(tmp_dir)
    os.remove(zip_path)

    if sub:
        zip_name = f'{sub}.zip'
        zip_path = os.path.join(tmp_dir, zip_name)
        for entry in os.scandir(tmp_dir):
            if entry.name != zip_name:
                os.remove(entry.path)            
        with zipfile.ZipFile(zip_path) as zip:
            zip.extractall(tmp_dir)
        os.remove(zip_path)

    g = load_gtfs(name, tmp_dir, minified_path)
    shutil.rmtree(tmp_dir)
    return g