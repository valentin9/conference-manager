# -*- coding: utf-8 -*-
#!/usr/bin/env python

import datetime
import pytest

from conferences import TimeUtils
from conferences import EventManager
from conferences import TimeSpan
from conferences import Event
from conferences import LunchTime

track1 =  [
    TimeSpan('09:00 - 12:00'),
    LunchTime('12:00 - 13:00'),
    TimeSpan('13:00 - 17:00')
    ]

track2 =  [
    TimeSpan('09:00 - 12:00'),
    LunchTime('12:00 - 13:00'),
    TimeSpan('13:00 - 17:00')
    ]

wront_file_name = 'input2.txt'
test_input_file = 'input.txt'


class TestTimeUtils(object):
    def test_time_delta_from_string(self):
        """normal case test time conversion from string to timedelta"""
        line = 'Pair Programming vs Noise 45min'
        line2 = '45min Pair Programming vs Noise'
        time_delta = datetime.timedelta(0,45*60)
        assert TimeUtils.time_delta_from_string(line) == time_delta
        assert TimeUtils.time_delta_from_string(line2) == time_delta

    def test_seconds_to_time_object(self):
        """should return correct datetime object from int"""
        minutes = 45
        delta = datetime.timedelta(0,45*60)

        negative_int = -5
        negative_delta = datetime.timedelta(0,-5*60)

        assert TimeUtils.time_delta_from_int(minutes) == delta
        assert TimeUtils.time_delta_from_int(negative_int) == negative_delta



class TestEventManager():
    """test of class EventManager"""
    def test_parse_default(self):
        """test schedule with default_input.txt"""
        eventMan = EventManager(track1, track2)
        eventMan.schedule()
        time = datetime.datetime.strptime('10:00', '%H:%M')
        assert eventMan.tracks[0][0].event_list[1].start_time == time

    def test_with_one_track(self):
        eventMan = EventManager(track1)
        eventMan.schedule()
        time = datetime.datetime.strptime('10:00', '%H:%M')
        assert eventMan.tracks[0][0].event_list[1].start_time == time


class TestTimeSpan():
    """test of class TimeSpan"""
    def test_init(self):
        """test basic init variables"""
        ts_object = TimeSpan('09:00-12:00')
        assert ts_object.sum == datetime.timedelta(0,0)
        other_ts_object = TimeSpan('12:00-13:00')
        assert other_ts_object.duration == datetime.timedelta(0,60*60)

    def test_duration(self):
        """make sure duration calculation works"""
        ts_object = TimeSpan('09:00-12:00')
        assert ts_object.duration == datetime.timedelta(0,3*60*60)

    def test_add_event(self):
        time_span = TimeSpan('12:00-13:00')
        event = Event('Accounting-Driven Development 45min')
        time_span.add_event(event)
        assert time_span.event_list[0].length == datetime.timedelta(0,45*60)


class TestLunchTime():
    """test of class TestLunchTime"""
    def test_start_time(self):
        lunch = LunchTime('12:00-13:00')
        start_time = datetime.datetime.strptime('12:00', '%H:%M')
        assert lunch.start_time == start_time

    def test_duration(self):
        lunch = LunchTime('12:00-13:00')
        assert lunch.duration == datetime.timedelta(0,0)


class TestEvent():
    """test of class Event"""
    def test_description_assignment(self):
        test_line = 'Accounting-Driven Development 45min'
        event_object = Event(test_line)
        assert event_object.description == test_line

    def test_set_time(self):
        """set_time should fill self.time"""
        test_line = 'Accounting-Driven Development 45min'
        event_object = Event(test_line)
        start_time = datetime.datetime.strptime('10:00', '%H:%M')
        time_delta = datetime.timedelta(0,60*60)
        end_time = datetime.datetime.strptime('11:00', '%H:%M')

        event_object.set_time(start_time, time_delta)
        assert event_object.start_time == end_time
