__author__ = 'marc'

import unittest

from lib import load_flight_file
from settings import FLIGHT_PATHS_FILE

from Data import Stream

from settings import FLIGHT_PATHS_FILE_JSON
import json

class CocoJsonTest(unittest.TestCase):
    def setUp(self):

        with open(FLIGHT_PATHS_FILE_JSON) as json_file:
            raw_data = json.load(json_file)

        self.streams = []

        for stream in raw_data['streams']:
            self.streams.append(Stream(stream['start_point'], stream['end_point'], stream['consumption'], stream['index']))
        self.consumption = raw_data['consumption']
        self.average = raw_data['average']


    def test_flight_load_count(self):
        """
        test_json that there are 5000 flight streams
        """
        self.assertEquals(5000, len(self.streams))


    def test_flight_average_load(self):
        """
        test_json that the average distance of the 5000 flight streams is 304.6366
        """
        self.assertEquals(304.6366, self.average)


    def test_flight_consumption(self):
        """
        test_json that the consumption without a stream is 10 per mile
        """
        flight_paths = load_flight_file(FLIGHT_PATHS_FILE)
        self.assertEquals(10, self.consumption)
