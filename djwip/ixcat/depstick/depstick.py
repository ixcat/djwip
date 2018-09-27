#! /usr/bin/env python

'''
datajoint schema dependency checker -

lists schemas that are dependent on given schemas,
or lists/graphs schemas in general

usage: depstick.py [forward|reverse] schema ...
       depstick.py [list|graph]
'''

import os
import sys

import datajoint as dj
import networkx as nx


def usage_exit():
    print('usage: depstick.py [forward|reverse|list|graph] schema ...')
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


def schemalist(*args):
    ''' list schemas '''
    dbc = dj.connection.conn()

    for r in dbc.query('select schema_name from information_schema.schemata;'):
        print(r[0])


def graph(*args):
    ''' graph schema interdependencies '''
    dbc = dj.connection.conn()

    print('// fetching schema list...')
    lq = 'select schema_name from information_schema.schemata'
    ignore = {'tmp', 'innodb', 'mysql', 'information_schema',
              'performance_schema'}
    names = [r[0] for r in dbc.query(lq) if r[0] not in ignore]

    g = nx.DiGraph()

    fq = '''
    SELECT distinct(UNIQUE_CONSTRAINT_SCHEMA)
    FROM information_schema.REFERENTIAL_CONSTRAINTS
    where constraint_schema='{}';
    '''

    rq = '''
    SELECT distinct(CONSTRAINT_SCHEMA)
    FROM information_schema.REFERENTIAL_CONSTRAINTS
    where unique_constraint_schema='{}';
    '''

    for n in names:

        print('// processing schema {}...'.format(n))
        g.add_node(n)

        print('// ... forward dependencies'.format(n))
        for i in (fwd[0] for fwd in dbc.query(fq.format(n)) if fwd[0] != n):
            g.add_node(i)
            g.add_edge(n, i)

        print('// ... reverse dependencies'.format(n))
        for i in (rev[0] for rev in dbc.query(rq.format(n)) if rev[0] != n):
            g.add_node(i)
            g.add_edge(i, n)

    # return io.BytesIO(self.make_dot().create_png())
    print(nx.drawing.nx_pydot.to_pydot(g))


if __name__ == '__main__':

    if len(sys.argv) < 2:
        usage_exit()

    cmdmap = {
        'forward': depstick,
        'reverse': depstick,
        'list': schemalist,
        'graph': graph,
    }

    cmd = sys.argv[1]
    if cmd not in cmdmap:
        usage_exit()

    if os.path.exists('dj_local_conf.json'):
        dj.config.load('dj_local_conf.json')

    if cmdmap[cmd] == depstick:
        for sname in sys.argv[2:]:
            depstick(sname, cmd)
    else:
        cmdmap[cmd](sys.argv[2:])
