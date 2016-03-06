#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    from conferences import TimeSpan
    from conferences import LunchTime
    from conferences import EventManager
    from conferences import NetworkingTime

    track1 =  [
        TimeSpan('09:00 - 12:00'),
        LunchTime('12:00 - 13:00'),
        TimeSpan('13:00 - 17:00'),
        NetworkingTime('16:00 - 17:00')
        ]

    track2 =  [
        TimeSpan('09:00 - 12:00'),
        LunchTime('12:00 - 13:00'),
        TimeSpan('13:00 - 17:00'),
        NetworkingTime('16:00 - 17:00')
        ]

    EvMan = EventManager(track1, track2)
    EvMan.schedule()