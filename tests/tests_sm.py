__author__ = 'marc'
import unittest
import json

from settings import FLIGHT_PATHS_FILE_JSON
from settings import FLIGHT_PATHS_SMALL_TEST_FILE_JSON

from Data import Stream
from Data import StreamJsonCalculator

class CocoStreamCalculatorSmallTest(unittest.TestCase):

    def setUp(self):

        with open(FLIGHT_PATHS_SMALL_TEST_FILE_JSON) as json_file:
            raw_data = json.load(json_file)
        self.calculator = StreamJsonCalculator(raw_data)



    def test_small_set(self):

        with open(FLIGHT_PATHS_SMALL_TEST_FILE_JSON) as json_file:
            raw_data = json.load(json_file)
        calculator = StreamJsonCalculator(raw_data)

    def test_small_set_average(self):
        """
        test that the average stream distance in small set is 3.57142857143
        """

        self.assertAlmostEqual(3.57142857143, self.calculator.average, places=7, msg=None, delta=None)

    def test_small_set_get_next_stream(self):
        """
        test the routine that finds first stream ahead
        """
        self.assertEqual(0, self.calculator.get_next_stream(0))
        self.assertEqual(4, self.calculator.get_next_stream(12))

    def test_small_set_next_streams_in_range(self):
        """
        test the routine that collects next streams within range
        """
        self.assertEquals([0,1,2,3], self.calculator.get_next_streams_in_range(0))
        self.assertEquals([2,3], self.calculator.get_next_streams_in_range(3))
        self.assertEquals([4], self.calculator.get_next_streams_in_range(7))
        self.assertEquals([4, 5], self.calculator.get_next_streams_in_range(9))
        self.assertEquals(None, self.calculator.get_next_streams_in_range(22))
        self.assertEquals(None, self.calculator.get_next_streams_in_range(30))

    def test_small_set_clean_next_streams_in_range(self):
        """
        test the routine that removes bad next streams
        """


        self.assertEquals([1,2,3], self.calculator.clean_next_streams(0, self.calculator.get_next_streams_in_range(0)))
    def test_small_set_sort_on_cost_clean_next_streams_in_range(self):
        """
        test the routine that removes bad next streams
        """


        self.assertEquals([1,2,3], self.calculator.sort_cleaned_streams_on_cost(0, self.calculator.clean_next_streams(0, self.calculator.get_next_streams_in_range(0))))
    def test_small_set_path(self):
        """
        test the paths routine
        """


        self.assertEquals([0,3,4,5], self.calculator.path(22))
    def test_small_set_consumption(self):
        """
        test the consumption calculation routine 22 miles consumes  352
        """


        self.assertEquals(352, self.calculator.fuel_consumption(self.calculator.path(22), 22))