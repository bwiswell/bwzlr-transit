# bwzlr-transit

`bwzlr-transit` is a lightweight Python package designed for fetching, parsing, and stripping down General Transit Feed Specification (GTFS) data to provide speedy Pythonic handling and querying about route, trip, and schedule information in a local context. No more messy and cross-referential GTFS datasets full of `.csv` files or SQL-based ORM libraries - just use `bt.fetch_gtfs` to fetch, parse, and transform your favorite transit agency's GTFS feed into a clean and monolithic `.json`-based mGTFS (Minified General Transit Feed Specification) dataset in seconds.

## Contents

- [Overview](#overview)
    - [mGTFS](#mgtfs)
- [Setup](#setup)
- [Usage](#usage)
    - [Fetching remote GTFS data](#fetching-remote-gtfs-data)
    - [Loading local GTFS data](#loading-local-gtfs-data)
    - [Loading local mGTFS data](#loading-local-minified-gtfs-data)
    - [Loading local mGTFS data with fallbacks](#loading-local-minified-gtfs-data-with-fallbacks)
    - [Saving mGTFS data](#saving-minified-gtfs-data)
- [Example](#example)

## Overview

### MGTFS
`bwzlr-transit` prioritizes I/O and query speed for journey planning via GTFS data, ignoring and discarding GTFS data other than agencies, routes, schedules, stops, and trips.

Typical GTFS data consists of a `.zip` of many `.csv` files, each containing a database table:

```txt
gtfs.zip
    agency.csv
    calendar.csv
    calendar_dates.csv
    ...
```

mGTFS is a minimal representation of the parts of these tables relevant to queries about agency, route, schedule, stop, and trip stored in a single `.json` file.

```json
{
    "name": "dataset-name",
    "feed": {
        ...
    },
    "agencies": {
        "agency-a": {
            ...
        },
        ...
    },
    "routes": {
        "route-a": {
            ...
        },
        ...
    },
    "schedules": {
        "service-a": {
            ...
        },
        ...
    },
    "stops": {
        "stop-a": {
            ...
        },
        ...
    },
    "trips": {
        "trip-a": {
            ...
        },
        ...
    }
    ...
}
```


## Setup
```sh
poetry add git+https://www.github.com/bwiswell/bwzlr-transit.git
```

## Usage

### Fetching remote GTFS data
```python
import bwzlr_transit as bt

gtfs = bt.fetch_gtfs(
    name = 'your-dataset-name',                         # Name of the GTFS dataset
    gtfs_uri = 'https://www.example.com/gtfs/data.zip', # URI of the GTFS dataset
    gtfs_sub = 'subdirectory',                          # Optional, for nested GTFS datasets
    mgtfs_path = 'path/to/minified/data.json'           # Optional, path to save minified data
)
```

### Loading local GTFS data
```python
import bwzlr_transit as bt

gtfs = bt.load_gtfs(
    name = 'your-dataset-name',                         # Name of the GTFS dataset
    gtfs_path = 'path/to/gtfs/data',                    # Local path to the GTFS dataset
    mgtfs_path = 'path/to/minified/data.json'           # Optional, path to save minified data
)
```

### Loading local minified GTFS data
```python
import bwzlr_transit as bt

gtfs = bt.load_mgtfs(
    mgtfs_path = 'path/to/minified/gtfs/data'           # Local path to the minified GTFS dataset
)
```

### Loading local minified GTFS data with fallbacks
```python
import bwzlr_transit as bt

gtfs = bt.load(
    name = 'your-dataset-name',                         # Name of the GTFS dataset
    gtfs_path = 'path/to/gtfs/data',                    # Optional, local path to the GTFS dataset
    gtfs_sub = 'subdirectory',                          # Optional, for nested GTFS datasets
    gtfs_uri = 'https://www.example.com/gtfs/data.zip', # Optional, URI of the GTFS dataset
    mgtfs_path = 'path/to/minified/gtfs/data'           # Optional, local path to the load/save the mGTFS
)
```

### Saving minified GTFS data
```python
import bwzlr_transit as bt

bt.save_mgtfs(
    gtfs = your_gtfs_data,                              # The GTFS object to write to file
    mgtfs_path = 'path/to/minified/gtfs/data'           # The path to save the minified data
)
```

## Example
```python
import bwzlr_transit as bt

GTFS_URI = 'https://www3.septa.org/developer/gtfs_public.zip'

gtfs = bt.fetch_gtfs(
    name = 'septa', 
    uri = GTFS_URI, 
    sub = 'google_rail',
    mpath = 'your/minified/gtfs/path.json'
)
```