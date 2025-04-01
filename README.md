# bwzlr-transit

`bwzlr-transit` is a lightweight Python package designed for fetching, parsing, and stripping down General Transit Feed Specification (GTFS) data to provide speedy Pythonic handling and querying about route, trip, and schedule information in a local context. No more messy and cross-referential GTFS datasets full of `.csv` files or SQL-based ORM libraries - just use `bt.fetch_gtfs` to fetch, parse, and transform your favorite transit agency's GTFS feed into a clean and monolithic `.json`-based mGTFS (Minified General Transit Feed Specification) dataset in seconds.

## Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)

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

`bt.GTFS` is the root object for handling GTFS data. the `bt.GTFS` object can be created from local or remote sources using `bt.GTFS.load`, and automatically handles parsing and converting the GTFS dataset to mGTFS. the resulting `bt.GTFS` object can be written out to a `.json` file using `bt.GTFS.save`.

#### Loading with `bt.GTFS.load`

If using a local mGTFS resource (preferred), `mgtfs_path` must be provided. If `mgtfs_path` is provided and no existing mGTFS dataset is found at the specified location, loading falls back to the options below. If loading is successful using one of those options, the minified version of the retrieved data will be saved to `mgtfs_path` to improve subsequent load times.

If using a local GTFS resource, `gtfs_path` must be provided. The GTFS data should already be unzipped.

If using a remote resource, `gtfs_uri` must be provided. `gtfs_sub` can optionally be provided to specify a subdirectory of the remote resource. `bt.GTFS.load` expects remote resources to be `.zip` files, or a `.zip` file of `.zip` files.

```python
import bwzlr_transit as bt

gtfs = bt.GTFS.load(
    name = 'your-dataset-name',                         # Name of the GTFS dataset
    gtfs_path = 'path/to/gtfs/data',                    # Optional, local path to the GTFS dataset
    gtfs_sub = 'subdirectory',                          # Optional, for nested GTFS datasets
    gtfs_uri = 'https://www.example.com/gtfs/data.zip', # Optional, URI of the GTFS dataset
    mgtfs_path = 'path/to/minified/gtfs/data'           # Optional, local path to the mGTFS dataset
)
```