import os
import shutil

from .api import fetch_gtfs, load_gtfs, load_minified_gtfs, save_minified_gtfs
from .gtfs import GTFS

__version__ = '0.1.0'


_TMP = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'tmp')

if os.path.exists(_TMP): shutil.rmtree(_TMP)