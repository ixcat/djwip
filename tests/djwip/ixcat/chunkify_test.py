

from importlib import reload
import logging

import datajoint as dj

from nose.tools import assert_true,  assert_false, assert_equals, raises


from djwip.ixcat.chunkify import InsertBuffer


from . import chunkify_schema
from .chunkify_schema import schema
from .chunkify_schema import TestTable


log = logging.getLogger(__name__)


def setup():
    schema.drop(force=True)
    reload(chunkify_schema)
    dj.config['safemode']=False


def teardown():
    TestTable().delete()


def test_test_table():
    t = TestTable()
    assert_equals(len(t), 0)
    TestTable.insert1((0, 'zero'))
    assert_equals(len(t), 1)
    TestTable.delete()
    assert_equals(len(t), 0)


def test_insertbuffer_insert1():
    teardown()

    ib = InsertBuffer(TestTable)
    nrec = 103
    
    for x in range(nrec):
        ib.insert1((x,'item {}'.format(x)))
        if ib.flush(chunksz=10):
            log.debug('chunked at item {}'.format(x))
            assert_equals(len(TestTable()) % 10, 0)

    if ib.flush():
        log.debug('finished at item {}'.format(x))
        assert_equals(len(TestTable()), 103)


def test_insertbuffer_insert1_opts():
    teardown()

    nrec = 103
    ib = InsertBuffer(TestTable)

    for x in range(nrec):

        ib.insert1((x, 'item {}'.format(x)))
        ib.insert1((x, 'item {}'.format(x)))  # skip_duplicates

        # ignore_extra_fields requires dj .insert() support for same..
        # ib.insert1((x, 'item {}'.format(x), 0))  # ignore_extra_fields

        if ib.flush(chunksz=10, skip_duplicates=True):
            log.debug('chunked at item {}'.format(x))
            assert_equals(len(TestTable()) % 10, 0)

    if ib.flush(skip_duplicates=True):
        log.debug('finished at item {}'.format(x))
        assert_equals(len(TestTable()), 103)


def test_insertbuffer_insert():
    teardown()

    nrec_x = 10
    nrec_y = 10
    ib = InsertBuffer(TestTable)

    for x in range(1, nrec_x+1):
        x = x*10
        xy = [(x+y, 'record {}'.format(x*y)) for y in range(1,nrec_y+1)]
        ib.insert(xy)
        ib.flush()


def test_insertbuffer_insert_opts():
    teardown()

    nrec_x = 10
    nrec_y = 10
    ib = InsertBuffer(TestTable)

    for x in range(1, nrec_x+1):
        x = x*10
        xy = [(x+y, 'record {}'.format(x*y)) for y in range(1,nrec_y+1)]
        xy = xy + xy
        ib.insert(xy)
        ib.flush(skip_duplicates=True)
