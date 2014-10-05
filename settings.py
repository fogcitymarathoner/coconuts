__author__ = 'marc'
import os

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
FLIGHT_PATHS_FILE = os.path.join(PROJECT_DIR, 'data', 'flight_paths.txt')
FLIGHT_PATHS_SMALL_TEST_FILE = os.path.join(PROJECT_DIR, 'data', 'flight_paths_small_test.txt')
FLIGHT_PATHS_FILE_JSON = os.path.join(PROJECT_DIR, 'data', 'flight_paths.json')
FLIGHT_PATHS_SMALL_TEST_FILE_JSON = os.path.join(PROJECT_DIR, 'data', 'flight_paths_small_test.json')
STREAMS_JSON = os.path.join(PROJECT_DIR, 'data', 'cleaned_streams.json')
FLIGHT_PATHS_ORIG_FILE_JSON = os.path.join(PROJECT_DIR, 'data', 'flight_paths_orig.json')
FLIGHT_PATHS_ORIG_SKIPPED_FILE_JSON = os.path.join(PROJECT_DIR, 'data', 'streams_skipped.json')
TEST_FLIGHT_PATHS_FILE = os.path.join(PROJECT_DIR, 'data', 'test_flight_paths.txt')
DEBUG=False