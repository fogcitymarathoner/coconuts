__author__ = 'marc'

import unittest
import json

from settings import FLIGHT_PATHS_FILE_JSON
from settings import FLIGHT_PATHS_SMALL_TEST_FILE_JSON

from Data import Stream
from Data import StreamJsonCalculator

class CocoStreamCalculatorNextTest(unittest.TestCase):

    def setUp(self):

        with open(FLIGHT_PATHS_FILE_JSON) as json_file:
            raw_data = json.load(json_file)
        self.calculator = StreamJsonCalculator(raw_data)

    def test_start_point_streams_list(self):
        """
        start_point_streams_list - tests list of streams just outside of end point
        within 2 average distances sorted on efficiency
        """
        stream = Stream(3478, 4060, 2910, 17)
        base_line = [19, 18, 20, 22, 21, 24, 23, 25]
        """
        next_list = self.calculator.start_point_streams_list(stream.start_point, stream)

        self.assertEquals(8, len(next_list))
        self.assertEquals(base_line, next_list)
                """


    def test_get_next_stream(self):
        """
        test the routine that finds first stream ahead
        """

        with open(FLIGHT_PATHS_FILE_JSON) as json_file:
            raw_data = json.load(json_file)
        calculator = StreamJsonCalculator(raw_data)
        self.assertEqual(0, calculator.get_next_stream(10))
        self.assertEqual(1, calculator.get_next_stream(400))
        self.assertEqual(9, calculator.get_next_stream(1200))
        self.assertEqual(17, calculator.get_next_stream(3000))
        self.assertEqual(46, calculator.get_next_stream(10000))
        self.assertEqual(152, calculator.get_next_stream(30000))


    def test_next_streams_in_range(self):
        """
        test the routine that collects next streams within range
        """

        with open(FLIGHT_PATHS_FILE_JSON) as json_file:
            raw_data = json.load(json_file)
        calculator = StreamJsonCalculator(raw_data)

        self.assertEquals([0,1,2,3], calculator.get_next_streams_in_range(0))
        self.assertEquals([0,1,2,3], calculator.get_next_streams_in_range(3))
        self.assertEquals([0,1,2,3], calculator.get_next_streams_in_range(7))
        self.assertEquals([0,1,2,3], calculator.get_next_streams_in_range(9))
        self.assertEquals([0,1,2,3], calculator.get_next_streams_in_range(22))
        self.assertEquals([0,1,2,3], calculator.get_next_streams_in_range(30))
        self.assertEquals([4,5,6,7,8], calculator.get_next_streams_in_range(500))
        self.assertEquals(None, calculator.get_next_streams_in_range(1000000))


    def test_path(self):
        """
        test the paths routine
        """


        self.assertEquals([0,6,8], self.calculator.path(1000))

    def test_small_set_consumption(self):
        """
        test the consumption calculation routine 22 miles consumes  352
        """


        self.assertEquals(220, self.calculator.fuel_consumption(self.calculator.path(22), 22))