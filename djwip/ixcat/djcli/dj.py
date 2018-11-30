#! /usr/bin/env python

import sys

from os.path import basename
from getopt import getopt, GetoptError
from code import interact
from collections import ChainMap

import datajoint as dj


app = basename(sys.argv[0])

def usage():
    use = 'usage: {} [-u user] [-p password] [-h host] [-s db:schema ...]'
    print(use.format(app))

if __name__ == '__main__':
    user, pw, host, opts, mods = (None, None, None, [], {})

    try:
        opts, rest = getopt(sys.argv[1:], 'u:p:h:s:')
    except GetoptError:
        usage()
        sys.exit()

    for o in opts:
        k, v = o

        if k == '-u':
            dj.config['database.user'] = v
        if k == '-p':
            dj.config['database.password'] = v
        if k == '-h':
            dj.config['database.host'] = v
        if k == '-s':
            d, m = v, v
            if ':' in v:
                d, m = v.split(':')
            mods[m] = dj.create_virtual_module(m, d)

    banner = 'dj repl\n'
    if mods:
        modstr = '\n'.join('  - {}'.format(m) for m in mods)
        banner += '\nschema modules:\n\n' + modstr + '\n'

    interact(banner, local=dict(mods, dj=dj))

