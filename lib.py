from __future__ import division

from settings import FLIGHT_PATHS_FILE
from settings import STREAMS_JSON
from settings import DEBUG
from settings import FLIGHT_PATHS_ORIG_FILE_JSON
from settings import FLIGHT_PATHS_ORIG_SKIPPED_FILE_JSON
import json

__author__ = 'marc'
def fun(x):
    return x + 1

def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

def load_flight_file(file=FLIGHT_PATHS_FILE):
    file = open(file, 'r')
    file_array = file.readlines()
    consumption = int(file_array[0])
    stream_array = []
    streams_indexes = range(1, len(file_array))
    for i in streams_indexes:
        l = file_array[i]
        stream_input_array = l.split()
        start_point = int(stream_input_array[0])
        end_point = int(stream_input_array[1])
        consumed = int(stream_input_array[2])
        efficiency = (end_point - start_point)/consumed
        stream_array.append([start_point, end_point, consumed, efficiency])

    return {
        'consumption': consumption,
        'streams': stream_array
    }

def sort_streams_on_start_point(stream_array):
    """
    sorts an array of streams on start point = [0]
    """
    return sorted(stream_array, key=lambda l: l[0])

def sort_streams_on_efficiency(stream_array):
    """
    sorts an array of streams decending on cost = [3]
    """
    return sorted(stream_array, key=lambda l: l[3])

def check_bad_next_streams(stream_array):
    """
    make sure all next streams in list are within current stream
    """
    # loop through all but last
    streams_indexes = range(0, len(stream_array) - 1)

    for i in streams_indexes:
        if stream_array[i + 1][0] > stream_array[i][1]:
            return False
    return True

def starts_inside(current_stream, next_stream):
    """
    return True if next stream starts in current stream
    """
    if next_stream[0] <= current_stream[1]:
        return True
    else:
        return False
def ends_outside(current_stream, next_stream):
    """
    return True if next stream starts in current stream
    """
    if next_stream[1] > current_stream[1]:
        return True
    else:
        return False

def good_next_candidate(i, j, stream_array):
    """
    returns True if j is a good next candidate for i
    """
    return starts_inside(stream_array[i], stream_array[j]) and ends_outside(stream_array[i], stream_array[j])
def throw_away_unproductive_next_streams(stream_array):
    """
    throw away all next streams that do not have an end point out side of current stream
    sorted on start_point
    """
    # cleaned stream array
    cleaned_streams = []
    skipped_streams = []
    # start with the first stream
    cleaned_streams.append(stream_array[0])

    i = 0
    j = 0
    while i < len(stream_array) and j < len(stream_array):
        j = i + 1
        while j < len(stream_array):

            if good_next_candidate(i, j, stream_array):
                cleaned_streams.append(stream_array[j])
                i += 1
                j += 1
            else:

                skipped_streams.append(stream_array[j])
                i += 1
                j += 1
                break

    return {
        'cleaned_streams': cleaned_streams,
        'skipped_streams': skipped_streams
    }

def streams_average(streams):
    """
    get average stream distance from a stream list
    """
    count = 0
    sum = 0
    for i in streams:
        sum += i[1] - i[0]
        count += 1
    return sum/count