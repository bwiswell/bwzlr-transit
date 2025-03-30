# bwzlr-transit

## Python

### Setup
```sh
poetry add git+https://www.github.com/bwiswell/bwzlr-transit.git
```

### Usage
```python
from datetime import date

import bwzlr_transit as bt

gtfs = bt.GTFS('Dataset Name', 'path/to/gtfs/data')
```