

import numpy as np
import datajoint as dj

from datajoint.blob import pack
from datajoint.hash import long_hash

# dj.config

schema = dj.schema('test_extfsck')

# fsckdb.schema.external_table.fetch()


@schema
class FsckData(dj.Lookup):
    definition = '''
    id:                 integer         # id
    ---
    data:               external        # test data
    hash:               char(43)        # local hash copy
    '''
    nrecs = 10

    class FsckPart(dj.Part):
        definition = '''
        -> FsckData
        ---
        junk:           external        # junk data
        '''

    @staticmethod
    def mkone(i):
        one = np.random.random(10)
        hsh = long_hash(pack(one))
        return (i, one, hsh)

    @property
    def contents(self):

        return (self.mkone(i) for i in range(self.nrecs))

    def populate(self):
        if not FsckData.FsckPart():
            recs = [(r[0], self.mkone(r[0])[1],) for r in FsckData.fetch()]
            FsckData.FsckPart.insert(recs)

    def corrupt(self):

        failtype = ['rmfile', 'chgfile', 'appendfile']
        failures = np.random.randint(0, self.nrecs, len(failtype))
        hashes = self.fetch('hash')

        for ft, fi in zip(failtype, failures):
            # todo: actually corrupt the files
            h = hashes[fi]

            if ft == 'rmfile':
                print('rmfile', h)

            if ft == 'chgfile':
                print('chgfile', h)

            if ft == 'appendfile':
                print('appendfile', h)
