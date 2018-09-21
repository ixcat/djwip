#! /usr/bin/env python

'''
datajoint external data fsck(8)-style utility.

usage: fsck.py schema ...

expects to be run with externals / db configured to match expected environment.

example output:

    $  ./fsck.py test_extfsck
    Connecting chris@localhost:3306
    checking test_extfsck.#fsck_data
    ... (9, '33_uJ_yrp4eLxb0Wpl81vIlzV5K-VBFf8pbghdG0WTI'): OK!
    ... (4, 'aNosXvCO5k50wiuiPoUxiec0c0QcDvNq-V4heYMuUaA'): OK!
    ... (6, 'gasjuBvBr0rjVUNYyB80WUlREKLHDcU5QHiTfgEIDc0'): OK!
    ... (8, 'KFDS3OtpwrrJv0HOxKT4Wj5Iyg7XCTTNllLf70x-H6c'): size mismatch
    ... (5, 'M4Uv2Wflan5jrRfapVJzlA_qHZSIL4NHTUNfYg_WTFc'): OK!
    ... (3, 'Q7p1SAp4TOD51FEeJzJWlWs4fIZE-5hR5d-OI1iQmUA'): OK!
    ... (0, 'SFzghvYiTSOmEs3qI1abto4qr2fUEqJJmaFw6bYmEd8'): OK!
    ... (2, 'tZy712Z24Y_d6CH35Sf0kQf7q_pgmv9ZiIFM-fUxGg4'): missing file /tmp/foo/test_extfsck/tZy712Z24Y_d6CH35Sf0kQf7q_pgmv9ZiIFM-fUxGg4
    ... (7, 'UQTurgINzbGhD4I4E8xuGt02UAkMzeU5fcazfVy3qhk'): OK!
    ... (1, 'uWJ9mZNzTv4oQYjlvaJ5D0rqHGiCdnhF35UDXrZxtH4'): hash mismatch

todo:
  - fix for part tables. notes:
        if isinstance(rel,str):
                rel = eval(rel)```

        in `table_to_class` :
        try:
                return schema.context[tname]
            except:
                # part table?
                return tname
  - performance
  - reimplement within dj.ExternalTable like the cleanup logic
'''

import sys
import re

import datajoint as dj

from datajoint import DataJointError
from datajoint.blob import pack
from datajoint.hash import long_hash

from pymysql import IntegrityError

from djwip.ixcat.schemax import schema_iterator


def usage_exit():
    print('usage: fsck.py schema ...')
    sys.exit(0)


def check_table(schema, rel):

    conn = rel.connection
    db = rel.database
    tab = rel.table_name
    hdr = rel.heading
    key = rel.primary_key

    print('checking {}.{}'.format(db, tab))

    ext = [b for b in hdr.blobs if hdr.attributes[b].type == 'external']

    if not ext:
        print('... skipping {}.{} - no external fields', db, tab)
        return

    for e in ext:
        fields = [*key, e]
        q = 'select {} from `{}`.`{}`'.format(','.join(fields), db, tab)
        for r in conn.query(q):
            try:
                h = r[len(fields)-1]
                b = schema.external_table.get(h)

                # can get None in some cases.. not sure when/where why.
                # XXX: slooow.. double pack
                if b is None or h != long_hash(pack(b)):
                    raise IntegrityError('hash mismatch')

                print('... {}: OK!'.format(r))  # todo: verbose flag?
            except AssertionError:
                print('... {}: size mismatch'.format(r))
            except IntegrityError:
                print('... {}: hash mismatch'.format(r))
            except DataJointError as e:
                matched = False
                for m in [re.match('^Lost.*?blob (.*)\.$', str(e))]:
                    print('... {}: missing file {}'.format(r, m.groups()[0]))
                    matched = True
                if not matched:
                    raise


def fsck(sname):
    '''
    check routine.

    XXX: could be faster/more granular if external checks done at lower level;
    this is skipped for code simplicity / modularity.
    '''

    mod = dj.create_virtual_module(sname, sname)

    schema = mod.schema

    for rel in schema_iterator(schema):

        check_table(schema, rel)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        usage_exit()

    for sname in sys.argv[1:]:
        fsck(sname)
