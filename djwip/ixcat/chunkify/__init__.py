'''
datajoint chunkifier -
wrap a datajoint auto-populate relation for chunked operation.
this is intended to allow improved performance for single-insert population
when latency is a factor by batching database interactions in groups

status: WIP/incomplete
'''
import datajoint as dj
from tqdm import tqdm
import logging


log = logging.getLogger(__name__)


class InsertBuffer(object):
    '''
    InsertBuffer: a utility class to help managed chunked inserts

    Currently requires records do not have prerequisites.
    '''
    def __init__(self, rel, chunksz=1, **insert_args):
        self._rel = rel
        self._queue = []
        self._chunksz = chunksz
        self._insert_args = insert_args

    def insert1(self, r):
        self._queue.append(r)

    def insert(self, recs):
        self._queue += recs

    def flush(self, chunksz=None):
        '''
        flush the buffer
        XXX: also get pymysql.err.DataError, etc - catch these or pr datajoint?
        XXX: optional flush-on-error? hmm..
        '''
        qlen = len(self._queue)
        if chunksz is None:
            chunksz = self._chunksz

        if qlen > 0 and qlen % chunksz == 0:
            try:
                self._rel.insert(self._queue, **self._insert_args)
                self._queue.clear()
                return qlen
            except dj.DataJointError as e:
                raise

    def __enter__(self):
        return self

    def __exit__(self, etype, evalue, etraceback):
        if etype:
            raise evalue
        else:
            return self.flush(1)


class ChunkyTable(dj.Table):
    ''' todo: implement, test '''

    def __init__(self, rel, chunksz=100):
        self.rel = rel
        self.chunkz = chunksz
        self.iqueue = []
        raise NotImplementedError('not complete')

    def insert1(self, rec):
        pass

    def insert(self, recs):
        [self.insert1(r) for r in recs]

    def make(self, key):
        self.rel.make(self)

    def populate(self):
        keys = self.rel.fetch(dj.key)
        chunks = [keys[i:i + self.chunksz]
                  for i in range(0, len(keys), self.chunksz)]
        for chunk in tqdm(chunks, total=len(chunks), unit_scale=self.chunksz):
            pass
