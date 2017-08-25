

from os.path import join as pathjoin
from os.path import dirname, abspath

import djwip.ixcat


columnar_data = [
    ['name', 'password', 'uid', 'gid', 'gecos', 'home_dir', 'shell'],
    ['root', 'VwL97VCAx1Qhs', '0', '1', '', '/', ''],
    ['daemon', 'x', '1', '1', '', '/', ''],
    ['sys', '', '2', '2', '', '/usr/sys', ''],
    ['bin', '', '3', '3', '', '/bin', ''],
    ['uucp', '', '4', '4', '', '/usr/lib/uucp', '/usr/lib/uucico'],
    ['dmr', '', '7', '3', '', '/usr/dmr', ''],
]

kv_data = [
    ['name', "User's login name."],
    ['password', "User's encrypted password."],
    ['uid', "User's login user ID."],
    ['gid', "User's login group ID."],
    ['gecos', 'General information about the user.'],
    ['home_dir', "User's home directory."],
    ['shell', "User's login shell."],
]


def cmp_2d(a, b):
    for row in zip(a, b):
        return False not in [col[0] == col[1] for col in zip(row[0], row[1])]


def test_csvbase():
    columnar = pathjoin(dirname(abspath(__file__)), 'columnar.csv')
    cb = djwip.ixcat.CSVBase(columnar)
    assert cmp_2d(columnar_data, cb) is not False


def test_csvcolumdict():
    columnar = pathjoin(dirname(abspath(__file__)), 'columnar.csv')
    cc = djwip.ixcat.CSVColumnDict(columnar)
    for row in columnar_data[1:]:
        ref = dict([(k, v) for (k, v) in zip(columnar_data[0], row)])
        assert ref == cc.__next__()


def test_csvrowdict_lo():
    kv = pathjoin(dirname(abspath(__file__)), 'kv.csv')
    ch = next(djwip.ixcat.CSVRowDict(kv))
    assert dict(kv_data) == ch


def test_csvrowdict_hi():
    kv = pathjoin(dirname(abspath(__file__)), 'kv.csv')
    ch = djwip.ixcat.CSVRowDict(kv).get()
    assert dict(kv_data) == ch


def test_csvrowdict_heading():
    kv = pathjoin(dirname(abspath(__file__)), 'kv.csv')
    ch = djwip.ixcat.CSVRowDict(kv, heading=True).get()
    assert dict(kv_data[1:]) == ch
