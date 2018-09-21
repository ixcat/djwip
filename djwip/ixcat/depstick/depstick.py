#! /usr/bin/env python

'''
datajoint schema dependency checker -

lists schemas that are dependent on given schemas,
or lists schemas in general

usage: depstick.py schema ...
'''

import os
import sys

import datajoint as dj


def usage_exit():
    print('usage: depstick.py [forward|reverse|list] schema ...')
    sys.exit(0)


def depstick(sname, direction='reverse'):
    ''' check/print report of dependencies '''
    vm = dj.create_virtual_module(sname, sname)
    dbc = vm.schema.connection

    # Constraint CONSTRAINT_NAME in CONSTRAINT_SCHEMA TABLE_NAME refers to
    # table REFERENCED_TABLE_NAME in UNIQUE_CONSTRAINT_SCHEMA.

    if direction == 'forward':
        q = '''
        SELECT distinct(UNIQUE_CONSTRAINT_SCHEMA)
        FROM information_schema.REFERENTIAL_CONSTRAINTS
        where constraint_schema='{}';
        '''.format(sname)

    elif direction == 'reverse':
        q = '''
        SELECT distinct(CONSTRAINT_SCHEMA)
        FROM information_schema.REFERENTIAL_CONSTRAINTS
        where unique_constraint_schema='{}';
        '''.format(sname)

    else:
        raise Exception("depstick doesn't know {} direction."
                        .format(direction))

    for r in dbc.query(q):
        print(r[0]) if r[0] != sname else None


def schemalist():
    ''' list schemas '''
    dbc = dj.connection.conn()

    for r in dbc.query('select schema_name from information_schema.schemata;'):
        print(r[0])


if __name__ == '__main__':

    if len(sys.argv) < 2:
        usage_exit()

    cmd = sys.argv[1]
    if cmd not in {'forward', 'reverse', 'list'}:
        usage_exit()

    if os.path.exists('dj_local_conf.json'):
        dj.config.load('dj_local_conf.json')

    if cmd != 'list':
        for sname in sys.argv[2:]:
            depstick(sname, cmd)
    else:
        schemalist()
