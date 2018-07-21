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
    def __init__(self, rel):
        self._rel = rel
        self._queue = []

    def insert1(self, r):
        self._queue.append(r)

    def insert(self, recs):
        self._queue += recs

    def flush(self, replace=False, skip_duplicates=False,
              ignore_extra_fields=False, ignore_errors=False, chunksz=1):
        '''
        flush the buffer
        XXX: use kwargs?
        XXX: ignore_extra_fields na, requires .insert() support
        '''
        qlen = len(self._queue)
        if qlen > 0 and qlen % chunksz == 0:
            try:
                self._rel.insert(self._queue, skip_duplicates=skip_duplicates,
                                 ignore_extra_fields=ignore_extra_fields,
                                 ignore_errors=ignore_errors)
                self._queue.clear()
                return True
            except dj.DataJointError as e:
                log.error('error in flush: {}'.format(e))
                raise


class ChunkyRelation(dj.BaseRelation):
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
