#! /usr/bin/env python

import os

from math import log
from math import modf
from time import time

import datajoint as dj

schema = dj.schema(os.environ['DJ_SCHEMA'])


@schema
class Event(dj.Manual):
    definition = """
    ev_sec:                     int
    ev_usec:                    int
    ---
    ev_note=NULL:               varchar(1024)
    """

    @classmethod
    def stampconv(cls, pytime):
        sec, usec = modf(pytime)
        sec = int(sec)
        usec = int(usec // 10 ** (int(log(usec, 10)) - 6 + 1))
        return sec, usec

    @classmethod
    def mkstamp(cls, note=None):
        sec, usec = Event.stampconv(time())
        return sec, usec, note

    def log_event(self, note=None):
        rec = Event.mkstamp(note)
        self.insert1(rec)
        return rec
