__author__ = 'marc'
import os
import sys
import inspect
import json
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
# put parent directory in path
sys.path.insert(0, parentdir)

from settings import FLIGHT_PATHS_FILE_JSON
from settings import FLIGHT_PATHS_SMALL_TEST_FILE
from settings import FLIGHT_PATHS_SMALL_TEST_FILE_JSON
from DataArray import StreamArrayCalculator
from lib import load_flight_file
# real data cache
raw_data = load_flight_file()
s = StreamArrayCalculator(raw_data)

f = open(FLIGHT_PATHS_FILE_JSON, 'w')

f.write(json.dumps(s.to_dict(), sort_keys=False, indent=4))
f.close()
# fake data cache
raw_data = load_flight_file(FLIGHT_PATHS_SMALL_TEST_FILE)
s = StreamArrayCalculator(raw_data)

f = open(FLIGHT_PATHS_SMALL_TEST_FILE_JSON, 'w')

f.write(json.dumps(s.to_dict(), sort_keys=False, indent=4))
f.close()
