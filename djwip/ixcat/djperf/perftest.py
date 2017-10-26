#! /usr/bin/env python

from importlib import reload

import datajoint as dj

dj.config['database.host'] = 'localhost'
dj.config['database.user'] = 'chris'
dj.config['database.schema'] = 'tutorial_bogus'

import perfschema as perf
perf.schema.drop(force=True)
reload(perf)

