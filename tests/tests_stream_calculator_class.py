__author__ = 'marc'

import unittest
import json

from settings import FLIGHT_PATHS_FILE_JSON
from settings import FLIGHT_PATHS_SMALL_TEST_FILE_JSON

from Data import Stream
from Data import StreamJsonCalculator

class CocoStreamCalculatorTest(unittest.TestCase):

    def setUp(self):

        with open(FLIGHT_PATHS_FILE_JSON) as json_file:
            raw_data = json.load(json_file)
        self.calculator = StreamJsonCalculator(raw_data)

    def test_init(self):
        """
        compare reloaded against cached
        """

        with open(FLIGHT_PATHS_FILE_JSON) as json_file:
            raw_data = json.load(json_file)
        calculator = StreamJsonCalculator(raw_data)
        self.assertEquals(10, calculator.consumption)
        self.assertEquals(5000, len(calculator.streams))
        with open(FLIGHT_PATHS_FILE_JSON) as json_file:
            raw_data = json.load(json_file)


    def test_start_on_stream(self):
        """
        test_json test if the journey starts on a stream
        """
        # small sample starts on stream
        with open(FLIGHT_PATHS_SMALL_TEST_FILE_JSON) as json_file:
            raw_data = json.load(json_file)
        calculator = StreamJsonCalculator(raw_data)
        self.assertTrue( calculator.start_on_stream())
        # big sample does not
        with open(FLIGHT_PATHS_FILE_JSON) as json_file:
            raw_data = json.load(json_file)
        calculator = StreamJsonCalculator(raw_data)
        self.assertNotEqual(True, calculator.start_on_stream())

    def test_path_within_first_stream(self):
        """
        test_json test if the journey starts on a stream
        """
        with open(FLIGHT_PATHS_SMALL_TEST_FILE_JSON) as json_file:
            raw_data = json.load(json_file)
        calculator = StreamJsonCalculator(raw_data)

        self.assertTrue( calculator.start_on_stream())


    def test_average(self):
        """
        test that the average stream distance in small set is 304.6366
        """

        with open(FLIGHT_PATHS_FILE_JSON) as json_file:
            raw_data = json.load(json_file)
        calculator = StreamJsonCalculator(raw_data)
        self.assertAlmostEqual(304.6366, calculator.average, places=7, msg=None, delta=None)
