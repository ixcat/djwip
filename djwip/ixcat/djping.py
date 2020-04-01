#! /usr/bin/env python

import os
import sys
import time

from textwrap import dedent
from socket import gethostbyname
from code import interact
from collections import ChainMap

import datajoint as dj
import pymysql as sql


DEFAULT_INTERVAL = 10


def usage_exit():
    me = os.path.basename(sys.argv[0])
    print(dedent('''
        usage: {} cmd args
          where 'cmd' one of:
            - ping [interval]: ping loop of interval seconds (default: {})
            - shell: interactive shell'''.format(
            me, DEFAULT_INTERVAL).strip('\n')))
          


def ping(interval=DEFAULT_INTERVAL):

    dj.conn()
    interval = int(interval)
    host = dj.config['database.host']
    ip = gethostbyname(host)

    print('DJPING {} ({}) every {}s.'.format(host, ip, interval))

    seq=0
    while True:

        try:

            start = time.time()
            dj.conn().ping()
            end = time.time()
            seq += 1

            print('djping from {}: seq={} time={:.3f}'.format( 
                ip, seq, end - start))

            time.sleep(interval)

        except sql.OperationalError as e:
            if e.args[0] == sql.constants.CR.CR_SERVER_LOST:
                print('connection lost. reconnecting.')
                dj.conn().connect()
                continue
            else:
                print('unknown error {}. reconnecting'.format(e.args))
                dj.conn().connect()
                continue

        except KeyboardInterrupt as k:
                return



def shell():
    interact('djping', local=dict(ChainMap(locals(), globals())))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        cmd_map = {
            'ping': ping,
            'shell': shell,
        }
        if cmd in cmd_map:
            cmd_map[cmd](*sys.argv[2:])
        else:
            usage_exit()
    else:
        ping()

