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
utd = bt.UTD.from_gtfs(gtfs)

# Show stations
for sid, station in utd.stations.items():
    print(f'{station.name}: {sid}')

trains_today = utd.on_date(date.today())
trains_connecting = trains_today.connecting('Station A ID', 'Station B ID')
print(trains_connecting)

utd.save('path/to/utd')
u = bt.UTD.load('path/to/utd')
```