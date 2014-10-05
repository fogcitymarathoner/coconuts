__author__ = 'marc'

import unittest
import json

from settings import FLIGHT_PATHS_FILE_JSON
from settings import FLIGHT_PATHS_SMALL_TEST_FILE
from DataArray import StreamArrayCalculator

from lib import load_flight_file
small_calculator_baseline = {'average': 3.5714285714285716, 'streams': [{'end_point': 5, 'start_point': 0, \
                                    'consumption': 10, 'index': 0}, {'end_point': 3, 'start_point': 1, 'consumption': 5,\
                                    'index': 1}, {'end_point': 7, 'start_point': 3, \
                                    'consumption': 12, 'index': 2}, {'end_point': 11, 'start_point': 6, 'consumption': 20, 'index': 3}, { \
                                    'end_point': 17, 'start_point': 14, 'consumption': 8, 'index': 4}, {'end_point': \
                                    24, 'start_point': 19, 'consumption': 14, 'index': 5}, {'end_point': 22, 'start_point': 21, \
                                    'consumption': 2, 'index': 6}], 'consumption': 50}
class CocoStreamArrayCalculatorTest(unittest.TestCase):

    def setUp(self):

        raw_data = load_flight_file()
        self.calculator = StreamArrayCalculator(raw_data)

    def test_init(self):
        """
        compare reloaded against cached
        """

        raw_data = load_flight_file()
        calculator = StreamArrayCalculator(raw_data)
        self.assertEquals(10, calculator.consumption)
        self.assertEquals(5000, len(calculator.streams))
        with open(FLIGHT_PATHS_FILE_JSON) as json_file:
            raw_data = json.load(json_file)
        calc_dict = calculator.to_dict()
        self.assertEquals(1140, calc_dict['streams'][5]['end_point'])
    def test_is_starts_within(self):
        """
        test_good_next - tests good_next to see if next candidate is good
        """
        self.assertFalse(self.calculator.is_starts_within(1051, 1050))
        self.assertTrue(self.calculator.is_starts_within(1051, 1052))
        self.assertTrue(self.calculator.is_starts_within(1051, 1053))
        self.assertTrue(self.calculator.is_starts_within(1051, 1054))
        self.assertFalse(self.calculator.is_starts_within(1051, 1055))

    def test_start_point_streams_list(self):
        """
        start_point_streams_list - tests list of streams containing start point
        """
        self.assertEquals(3, len(self.calculator.start_point_streams_list(211870)))
        self.assertEquals(1049, self.calculator.start_point_streams_list(211870)[0].index)
        self.assertEquals(1050, self.calculator.start_point_streams_list(211870)[1].index)
        self.assertEquals(1051, self.calculator.start_point_streams_list(211870)[2].index)

    def test_small_set_load(self):
        """
        test_json test that small test set loads
        """
        raw_data = load_flight_file(FLIGHT_PATHS_SMALL_TEST_FILE)
        calculator = StreamArrayCalculator(raw_data)
        self.assertEquals(small_calculator_baseline, calculator.to_dict())
