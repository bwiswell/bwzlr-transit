import json
import os
import shutil
from typing import Optional
from urllib import request
import zipfile

from .gtfs import GTFS, GTFS_SCHEMA
from .models import Feed
from .tables import Agencies, Routes, Schedules, Trips


def save_mgtfs (gtfs: GTFS, mgtfs_path: str):
    print('saving minified GTFS data...')
    data = GTFS_SCHEMA.dump(gtfs)
    with open(mgtfs_path, 'w') as file:
        json.dump(data, file)

def load_gtfs (
            name: str, 
            gtfs_path: str,
            mgtfs_path: Optional[str] = None
        ) -> GTFS:
    print('loading GTFS data...')
    g = GTFS(
        name=name, 
        feed=Feed.from_gtfs(gtfs_path),
        agencies=Agencies.from_gtfs(gtfs_path), 
        routes=Routes.from_gtfs(gtfs_path), 
        schedules=Schedules.from_gtfs(gtfs_path), 
        trips=Trips.from_gtfs(gtfs_path)
    )
    if mgtfs_path: save_mgtfs(g, mgtfs_path)
    return g

def load_mgtfs (mgtfs_path: str) -> GTFS:
    print('loading minified GTFS data...')
    data = {}
    with open(mgtfs_path, 'r') as file:
        data = json.load(file)
    return GTFS_SCHEMA.load(data)

def fetch_gtfs (
            name: str,
            gtfs_uri: str,
            mgtfs_sub: Optional[str] = None,
            mgtfs_path: Optional[str] = None
        ) -> GTFS:
    print(f'fetching GTFS data from {gtfs_uri}...')
    tmp_dir = os.path.join(
        os.path.realpath(os.path.dirname(__file__)),
        'tmp'
    )
    os.mkdir(tmp_dir)

    zip_path = os.path.join(tmp_dir, f'{name}.zip')
    request.urlretrieve(gtfs_uri, zip_path)
    with zipfile.ZipFile(zip_path) as zip:
        zip.extractall(tmp_dir)
    os.remove(zip_path)

    if mgtfs_sub:
        zip_name = f'{mgtfs_sub}.zip'
        zip_path = os.path.join(tmp_dir, zip_name)
        for entry in os.scandir(tmp_dir):
            if entry.name != zip_name:
                os.remove(entry.path)            
        with zipfile.ZipFile(zip_path) as zip:
            zip.extractall(tmp_dir)
        os.remove(zip_path)

    g = load_gtfs(name, tmp_dir, mgtfs_path)
    shutil.rmtree(tmp_dir)
    return g

def load (
            name: str,
            gtfs_path: Optional[str] = None,
            gtfs_sub: Optional[str] = None,
            gtfs_uri: Optional[str] = None,
            mgtfs_path: Optional[str] = None
        ) -> GTFS:
    if mgtfs_path and os.path.exists(mgtfs_path):
        return load_mgtfs(mgtfs_path)
    elif gtfs_path:
        return load_gtfs(name, gtfs_path, mgtfs_path)
    else:
        return fetch_gtfs(
            name, gtfs_uri, gtfs_sub, mgtfs_path
        )