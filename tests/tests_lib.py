__author__ = 'marc'

import unittest
from lib import streams_average
from lib import load_flight_file
from lib import sort_streams_on_start_point
from lib import check_bad_next_streams
from lib import throw_away_unproductive_next_streams
from lib import starts_inside
from lib import ends_outside
from lib import sort_streams_on_efficiency
from settings import TEST_FLIGHT_PATHS_FILE
from settings import FLIGHT_PATHS_FILE

from Data import Stream

baseline = {'streams': [[721882, 721948, 330, 0.2], [198623, 198930, 1228, 0.25], [293173,
 293753, 1740, 0.3333333333333333]], 'consumption': 10}
baseline_sorted_on_start_point = [
                    [198623, 198930, 1228, 0.25],
                    [293173, 293753, 1740, 0.3333333333333333],
                    [721882, 721948, 330, 0.2]
                ]
baseline_sorted_on_efficiency = [
                    [721882, 721948, 330, 0.2],
                    [198623, 198930, 1228, 0.25],
                    [293173, 293753, 1740, 0.3333333333333333],
]
baseline_sorted_on_start_point_one_bad_next_in_middle = [
                    [198623, 198930, 1228, 0.25],
                    [198930, 198940, 1740, 0.3333333333333333],
                    [198623, 198929, 1740, 0.3333333333333333],
                    [721882, 721948, 330, 0.2]
                ]
baseline_sorted_on_start_point_one_bad_next_in_end = [
                    [198623, 198930, 1228, 0.25],
                    [198930, 198940, 1740, 0.3333333333333333],
                    [198940, 198950, 1740, 0.3333333333333333],
                    [721882, 721948, 330, 0.2]
                ]
baseline_good_next_stream = [[198623, 198930, 1228, 0.25], [198930, 293753, 1740, 0.3333333333333333],
                   [293753, 721948, 330, 0.2]]
class CocoLibTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_stream_init(self):
        """
        test_stream_init - tests that the Stream Class initializes right
        """
        stream = Stream(0, 12, 1)
        base_line = {'consumption': 1, 'end_point': 12, 'start_point': 0, 'index': None, 'efficiency': 12}
        self.assertEqual(base_line, stream.to_dict())


    def test_flight_file_load(self):
        """
        test that original flight paths txt file loads
        """
        flight_paths = load_flight_file(TEST_FLIGHT_PATHS_FILE)
        self.assertEquals(baseline, flight_paths)


    def test_flight_load_count(self):
        """
        test that there are 5000 flight streams
        """
        flight_paths = load_flight_file(FLIGHT_PATHS_FILE)
        self.assertEquals(5000, len(flight_paths['streams']))


    def test_flight_average_load(self):
        """
        test that the average distance of the 5000 flight streams is 304.6366
        """
        flight_paths = load_flight_file(FLIGHT_PATHS_FILE)
        self.assertEquals(304.6366, streams_average(flight_paths['streams']))


    def test_flight_consumption(self):
        """
        test that the consumption without a stream is 10 per mile
        """
        flight_paths = load_flight_file(FLIGHT_PATHS_FILE)
        self.assertEquals(10, flight_paths['consumption'])

    def test_sort_streams_on_start_point(self):
        """
        test_sort_streams_on_start_point - test function that sorts stream on start points.
        """

        self.assertEquals(baseline_sorted_on_start_point, sort_streams_on_start_point(baseline['streams']))

    def test_sort_streams_on_efficiency(self):
        """
        test_sort_streams_on_efficiency - test function that sorts stream on start points.
        """

        self.assertEquals(baseline_sorted_on_efficiency, sort_streams_on_efficiency(baseline['streams']))

    def test_check_bad_next_streams(self):
        """
        test_check_bad_next_streams - test function that verifies that there are no gaps in streams
        """
        self.assertFalse(check_bad_next_streams(baseline['streams']))
        self.assertTrue(check_bad_next_streams(baseline_good_next_stream))
    def test_starts_inside(self):
        """
        """
        current = [0, 10, 333, 0]
        next_good = [10, 20, 333, 0]
        next_bad = [11, 20, 333, 0]

        self.assertTrue(starts_inside(current, next_good))
        self.assertFalse(starts_inside(current, next_bad))
    def test_ends_outside(self):
        """
        """
        current = [0, 10, 333, 0]
        next_good = [10, 20, 333, 0]
        next_bad = [5, 7, 333, 0]

        self.assertTrue(ends_outside(current, next_good))
        self.assertFalse(ends_outside(current, next_bad))
    def test_throw_away_unproductive_next_streams(self):
        """
        test_throw_away_unproductive_next_streams - test routine that throws away next streams not ending outside of current stream
        """
        # baseline_sorted_on_start_point doesn't have contiguous streams
        response = [[198623, 198930, 1228, 0.25]]
        self.assertEquals(response, throw_away_unproductive_next_streams(baseline_sorted_on_start_point)['cleaned_streams'])

        response = [[198623, 198930, 1228, 0.25], [198930, 198940, 1740, 0.3333333333333333]]

        self.assertEquals(response, throw_away_unproductive_next_streams(baseline_sorted_on_start_point_one_bad_next_in_middle)['cleaned_streams'])

        response = [[198623, 198930, 1228, 0.25], [198930, 198940, 1740, 0.3333333333333333], [198940, 198950, 1740, 0.3333333333333333]]

        self.assertEquals(response, throw_away_unproductive_next_streams(baseline_sorted_on_start_point_one_bad_next_in_end)['cleaned_streams'])
