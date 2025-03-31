# bwzlr-transit

## Setup
```sh
poetry add git+https://www.github.com/bwiswell/bwzlr-transit.git
```

## Usage

### Fetching remote GTFS data
```python
import bwzlr_transit as bt

gtfs = bt.fetch_gtfs(
    name = 'your-dataset-name',                     # Name of the GTFS dataset
    uri = 'https://www.example.com/gtfs/data.zip',  # URI of the GTFS dataset
    sub = 'subdirectory',                           # Optional, for nested GTFS datasets
    minified_path = 'path/to/minified/data.json'    # Optional, path to save minified data
)
```

### Loading local GTFS data
```python
import bwzlr_transit as bt

gtfs = bt.load_gtfs(
    name = 'your-dataset-name',                     # Name of the GTFS dataset
    path = 'path/to/gtfs/data',                     # Local path to the GTFS dataset
    minified_path = 'path/to/minified/data.json'    # Optional, path to save minified data
)
```

### Loading local minified GTFS data
```python
import bwzlr_transit as bt

gtfs = bt.load_minified_gtfs(
    path = 'path/to/minified/gtfs/data'             # Local path to the minified GTFS dataset
)
```

### Saving local minified GTFS data
```python
import bwzlr_transit as bt

bt.save_minified_gtfs(
    gtfs = your_gtfs_data,                          # The GTFS object to write to file
    path = 'path/to/minified/gtfs/data'             # The path to save the minified data
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
    minified_path = 'your/minified/gtfs/path.json'
)
```