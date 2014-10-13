__author__ = 'marc'
from lib import sort_streams_on_efficiency
class Stream:

    def __init__(self, start_point, end_point, consumption, index=None):
        self.start_point = start_point
        self.end_point = end_point
        self.efficiency = (end_point - start_point)/consumption
        self.consumption = consumption
        self.index = index

    def to_dict(self):
        return {
            'start_point': self.start_point,
            'end_point': self.end_point,
            'efficiency': self.efficiency,
            'consumption': self.consumption,
            'index': self.index
        }
class StreamJsonCalculator:
    """
    StreamJsonCalculator class
    """
    def __init__(self, raw_data):


        self.streams = []

        for stream in raw_data['streams']:
            self.streams.append(Stream(stream['start_point'], stream['end_point'], stream['consumption'], stream['index']))
        self.consumption = raw_data['consumption']
        self.average = raw_data['average']

    def start_on_stream(self):
        """
        returns True if the first stream starts on mile 0
        """
        if self.streams[0].start_point == 0:
            return True
        else:
            return False

    def get_next_stream(self, self_powered_point):
        """
        return next stream ahead of a self_powered_point
        """
        for s in self.streams:
            if s.start_point >= self_powered_point:
                return s.index

    def get_next_streams_in_range(self, self_powered_point):
        """
        return list of next streams within 5 average distances away
        """
        unsorted_uncleaned_streams = []
        outside_limit = self_powered_point + 5 * self.average
        start_point = self_powered_point
        # skip if start point is out of stream range
        if start_point > self.streams[len(self.streams)-1].end_point:
            return None
        index = self.get_next_stream(start_point)
        if index is not None:
            while index < len(self.streams) - 1:
                if self.streams[index].start_point < outside_limit:
                    unsorted_uncleaned_streams.append(
                        self.streams[index].index
                    )
                else:
                    break
                index += 1
            return unsorted_uncleaned_streams
        else:
            return None
    def clean_next_streams(self, self_powered_point, unsorted_uncleaned_streams):
        """
        remove next streams that contain the self_powered_point
        sort accending on cost
        """
        cleaned_streams = []

        for p in unsorted_uncleaned_streams:

            if not (self_powered_point >= self.streams[p].start_point and self_powered_point <= self.streams[p].end_point):
                cleaned_streams.append(p)
        return cleaned_streams
    def sort_cleaned_streams_on_cost(self, self_powered_start_point, unsorted_clean_streams):
        """
        sorts cleaned streams on cost accending
        """
        unsorted_full = []
        for i in unsorted_clean_streams:

            cost = self.streams[i].consumption + (self.streams[i].start_point - self_powered_start_point) * self.consumption

            unsorted_full.append([
                self.streams[i].start_point,
                self.streams[i].end_point,
                self.streams[i].consumption,
                cost,
                self.streams[i].index
            ])

        sorted_full = sort_streams_on_efficiency(unsorted_full)

        sorted_indexes = []
        for i in sorted_full:
            sorted_indexes.append(i[4])
        return sorted_indexes
    def path(self, end_point):
        """
        return path
        """
        streams = []
        streams.append(0)

        current_stream = 0
        # see if end_point reaches first stream, return empty path
        if end_point < self.streams[current_stream].end_point:
            return []
        else:
            current_point = self.streams[current_stream].end_point
        while current_point <= end_point:
            next_list = self.get_next_streams_in_range(current_point)

            sorted_list = self.sort_cleaned_streams_on_cost(current_point,
                                              self.clean_next_streams(current_point, next_list))
            # no good next paths
            if len(sorted_list) > 0:
                best_next = sorted_list[0]
                # done add if it's outside of end point
                if self.streams[best_next].start_point < end_point:
                    streams.append(best_next)
                    current_point = self.streams[best_next].end_point
                else:
                    break
            else:
                break
        return streams
    def fuel_consumption(self, paths, end_point):
        """
        return consumption on paths
        """
        # adjust start point if in stream
        current_stream = 0
        if self.start_on_stream():
            consumption = self.streams[current_stream].consumption
        else:

            if end_point > self.streams[current_stream].start_point:
                consumption = (self.streams[current_stream].start_point * self.consumption) + self.streams[current_stream].consumption

            if end_point < self.streams[current_stream].start_point:
                consumption = end_point * self.consumption

        current_point = self.streams[current_stream].end_point
        k = 0
        for i in paths[1:]:
            consumption += (self.streams[i].start_point - current_point) * self.consumption
            consumption += self.streams[i].consumption
            current_point = self.streams[i].end_point
            k = i
        # add the remainder if travel doesn't end in a stream
        if end_point > self.streams[k].end_point:
            consumption += (end_point - self.streams[k].end_point) * self.consumption
        return consumption