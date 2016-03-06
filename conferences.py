# -*- coding: utf-8 -*-
#!/usr/bin/env python

import re
import datetime
import itertools


INPUT_FILE = 'input.txt'
PRINT_TIME_FORMAT = '%I:%M%p'
SORT_BY_LENGTH = False
DISTRIBUTED_FIRST_FIT = True


Time = datetime.datetime
TimeDelta = datetime.timedelta


class TimeUtils(object):
    @staticmethod
    def time_obj_from_string(string):
        """
        return list with datetime-objects from a list
        or a string with a time stamp.
        """
        stripped = string.strip()
        parsed = Time.strptime(stripped, '%H:%M')
        return parsed

    @staticmethod
    def time_delta_from_string(line):
        """Extracts digit from string and return time in minutes"""
        try:
            result = re.search(r'\d+', line).group(0)
        except AttributeError:
            result = 5
        return TimeUtils.time_delta_from_int(result)

    @staticmethod
    def time_delta_from_int(number):
        """return timedelta object parsed from int"""
        seconds = int(number)*60
        return TimeDelta(0, seconds)


class EventManager(object):
    """
    Accepts lists:
    evMan = EventManager(
        [TimeSpan('12:00 - 13:00'),TimeSpan('12:00 - 13:00')],
        [TimeSpan('12:00 - 13:00'),TimeSpan('12:00 - 13:00')]
        )
    each argument(a list) is considered a track
    """
    def __init__(self, *tracks):
        self.filename = INPUT_FILE
        self.events_list = []
        self.tracks = list(tracks)
        tracks_count = len(self.tracks)
        self.cycle = itertools.cycle(range(0,tracks_count))

    def schedule(self):
        """wrapper to parse, schedule and print"""
        self.parse_events()
        if SORT_BY_LENGTH:
            self.sort_by_length()
        if DISTRIBUTED_FIRST_FIT:
            for item in self.events_list:
                self.distributed_first_fit(item)
        else:
            for item in self.events_list:
                self.simple_first_fit(item)
        self.update_variable_spans()
        self.print_schedule()

    def sort_by_length(self):
        self.events_list.sort(key=lambda x: x.length, reverse=True)


    def distributed_first_fit(self, event_item):
        """distribute events with "first fit" algorithm"""
        tracks_count = len(self.tracks)
        index = self.cycle.next()
        for time_span in self.tracks[index]:
            is_assigned = self.try_to_fit(time_span, event_item)
            if is_assigned:
                return True

    def simple_first_fit(self, event_item):
        """distribute events with "first fit" algorithm"""
        for track in self.tracks:
            for time_span in track:
                is_assigned = self.try_to_fit(time_span, event_item)
                if is_assigned:
                    return True

    def try_to_fit(self, _time_span, _event_item):
        potential_length = _time_span.sum + _event_item.length
        if potential_length <= _time_span.duration:
            _event_item.set_time(_time_span.start_time, _time_span.sum)
            _time_span.add_event(_event_item)
            return True

    def update_variable_spans(self):
        for track in self.tracks:
            last_event_time = None
            for span in track:
                try:
                    last_event_time = span.event_list[-1].end_time
                except:
                    span.update_times(last_event_time)

    def parse_events(self):
        """Parse input file and save items to self.events_list"""
        try:
            self.events_list = []
            with open(self.filename) as input_file:
                for event_description_line in input_file:
                    event = Event(event_description_line.rstrip())
                    self.events_list.append(event)
        except IOError, err:
            print IOError('File {} was not found'.format(self.filename))

    def print_schedule(self):
        for index, track in enumerate(self.tracks):
            print 'Track', index+1
            for time_span in track:
                time_span.print_description_line()
                for event_item in time_span.event_list:
                    event_item.print_description_line()


class TimeSpan(object):
    """
    TimeSpan accepts a string:
    new_span = TimeSpan("12:00 - 13:00")
    """
    def __init__(self, time_span_string):
        self.event_list = []
        self.sum = TimeDelta(0,0)
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.type = None
        self.construct_time_data(time_span_string)

    def construct_time_data(self, time_span_string):
        _start_time, _end_time = time_span_string.split("-")

        self.start_time = TimeUtils.time_obj_from_string(_start_time)
        self.end_time = TimeUtils.time_obj_from_string(_end_time)
        self.duration = self.end_time - self.start_time

    def add_event(self, item):
        self.event_list.append(item)
        self.sum += item.length

    def update_times(self, time):
        pass

    def print_description_line(self):
        pass


class LunchTime(TimeSpan):
    """
    TimeSpan Child class for break/lunch spans
    only difference is duration = 0
    """
    def __init__(self, time_span_string):
        super(LunchTime, self).__init__(time_span_string)
        self.type = 'Lunch'

    def construct_time_data(self, time_span_string):
        super(LunchTime, self).construct_time_data(time_span_string)
        self.duration = TimeDelta(0,0)

    def print_description_line(self):
        print self.start_time.strftime(PRINT_TIME_FORMAT),
        print self.type


class NetworkingTime(TimeSpan):
    """
    TimeSpan Child class for break/lunch spans
    only difference is duration = 0
    """
    def __init__(self, time_span_string):
        super(NetworkingTime, self).__init__(time_span_string)
        self.type = 'Networking Event'

    def construct_time_data(self, time_span_string):
        super(NetworkingTime, self).construct_time_data(time_span_string)
        self.duration = TimeDelta(0,0)

    def update_times(self, time):
        if time > self.start_time and time < self.end_time:
            self.start_time = time
            self.end_time = time + self.duration

    def print_description_line(self):
        print self.start_time.strftime(PRINT_TIME_FORMAT),
        print self.type


class Event(object):
    """Event data class, accepts description_line and sets data from it"""
    def __init__(self, description_line):
        self.description = description_line
        self.length = TimeUtils.time_delta_from_string(description_line)
        self.start_time = None
        self.end_time = None

    def set_time(self, span_start, seconds_from_start):
        _time = span_start + seconds_from_start
        self.start_time = _time
        self.end_time = self.start_time + self.length

    def print_description_line(self):
        print self.start_time.strftime(PRINT_TIME_FORMAT),
        print self.description
