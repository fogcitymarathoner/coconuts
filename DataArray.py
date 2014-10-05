__author__ = 'marc'
import json


from lib import load_flight_file

from lib import sort_streams_on_start_point
from lib import streams_average

from settings import FLIGHT_PATHS_FILE_JSON

from Data import Stream
class StreamArrayCalculator:

    def __init__(self, raw_data):


        sorted_streams = sort_streams_on_start_point(raw_data['streams'])
        """
        check_bad_next_streams(sorted_streams)
        unproductive_streams_removed = throw_away_unproductive_next_streams(sorted_streams)
        """
        self.streams = []
        i = 0
        for stream in sorted_streams:

            self.streams.append(Stream(stream[0], stream[1], stream[2], i))
            i += 1

        self.consumption = raw_data['consumption']
        self.average = streams_average(raw_data['streams'])

    def to_dict(self):
        streams = []
        for s in self.streams:

            stream = {
                "start_point": s.start_point,
                "end_point": s.end_point,
                "consumption": s.consumption,
                "index": s.index
            }
            streams.append(stream)
        return {'consumption': self.consumption,
                "average": self.average,
                'streams': streams
        }
    def is_starts_within(self, current_stream_index, next_candidate_stream_index):
        """
        return False if next_candidate start is out of current range
        """
        # True if next starts in current
        if self.streams[next_candidate_stream_index].start_point >= self.streams[current_stream_index].start_point and \
            self.streams[next_candidate_stream_index].start_point <= self.streams[current_stream_index].end_point:
            return True
        else:
            return False
    def start_point_streams_list(self, start_point):
        """
        start_point_streams_list - return list of streams containing start point.
        """
        streams_within = []
        for s in self.streams:
            # return streams at first start out of range
            if start_point < s.start_point:
                return streams_within
            if start_point <= s.end_point and start_point >= s.start_point:
                streams_within.append(s)
        return streams_within