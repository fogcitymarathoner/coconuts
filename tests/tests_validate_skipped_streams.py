__author__ = 'marc'

import unittest

from lib import load_flight_file
from lib import sort_streams_on_start_point
from lib import throw_away_unproductive_next_streams


class CocoSkippedStreamsTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_thrown_away_unproductive_next_streams(self):
        """
        test_throw_away_unproductive_next_streams - test routine that throws away next streams not ending outside of any starting string
        """

        streams_array = load_flight_file()
        raw_streams = streams_array['streams']
        # returns cleaned_streams and skipped_streams
        sorted_streams = sort_streams_on_start_point(raw_streams)

        #check_bad_next_streams(sorted_streams)
        res = throw_away_unproductive_next_streams(sorted_streams)
        cleaned_streams = res['cleaned_streams']
        skipped_streams = res['skipped_streams']
        for skipped in skipped_streams:
            count = 0
            for raw in raw_streams:
                # starting in
                if skipped[0] >= raw[0] and skipped[0] <= raw[1]:
                    # ending outside
                    if skipped[1] >= raw[1]:
                        count += 1
            self.assertGreater(count, 0)
