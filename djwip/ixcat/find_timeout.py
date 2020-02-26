#! /usr/bin/env python

import os
import sys
import time
import logging

from datetime import datetime
from code import interact
from collections import ChainMap

import datajoint as dj


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

schema = dj.schema('{}_find_timeout'.format(
    dj.config.get('database.user', 'test')))

#
# Timeout Schema
#


@schema
class TimeRange(dj.Lookup):
    definition = '''
    minutes:    int
    '''
    contents = zip(range(60))


@schema
class TestSession(dj.Manual):
    definition = '''
    test_session_id:         timestamp
    '''

    @classmethod
    def create(cls, start_time=None):

        rec = {'test_session_id': start_time if start_time
               else datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}

        log.info('creating TestSession {}'.format(rec))

        cls().insert1(rec)

        return rec


@schema
class TestRun(dj.Computed):
    definition = '''
    -> TestSession
    -> TimeRange
    '''

    def make(self, key):
        log.info('TestRun with {}'.format(key))
        time.sleep(key['minutes'] * 60)
        self.insert1(key)


#
# Application Logic
#

def run(*args):
    session = TestSession.create()
    TestRun.populate((TestSession * TimeRange & session), reserve_jobs=True,
                     suppress_errors=True)

    log.info('completed successfully!')


def multirun(*args):
    nruns = int(args[0]) if args else 10

    for i in range(nruns):
        log.info('multirun: beginning run {}'.format(i))

        try:
            run()
        except Exception as e:
            log.info('run {} encountered exception: {}'.format(i, repr(e)))

    log.info('multirun complete')


def shell(*args):
    interact('timeout shell', local=dict(ChainMap(locals(), globals())))


def results(*args):

    filt = args if args else {}

    result_data = (TestSession & filt).aggr(
        TestRun, max_mins='max(minutes)').fetch(
            order_by='test_session_id', as_dict=True)

    print('===============\t\t===========')
    print('test_session_id\t\tmax_minutes')
    print('===============\t\t===========')
    for r in result_data:
        print('{}\t{}'.format(r['test_session_id'], r['max_mins']))


if __name__ == '__main__':

    actions = {
        'run': run,
        'multirun': multirun,
        'shell': shell,
        'results': results,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in actions:
        print('usage: {} [run|shell]'.format(os.path.basename(sys.argv[0])))
        sys.exit(0)

    action = sys.argv[1]
    actions[action](*sys.argv[2:])
