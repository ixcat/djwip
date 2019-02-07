
import datajoint as dj

from . import InsertBuffer

schema = dj.schema('test_djwip_ixcat_chunkify')


@schema
class TestInsertBuffer(dj.Manual):
    definition = '''
    insertid: int
    '''

    def test(self):
        self.delete_quick()
        self.test_manual_buffer()
        self.test_context_buffer()
        assert(len(self) == 202)

    def test_manual_buffer(self):
        # using 'ignore_extra_fields' here as superflouous test of insert_args
        ib = InsertBuffer(self, chunksz=10, ignore_extra_fields=True)
        for x in range(101):
            ib.insert1((x,))
            print(ib._queue)
            if ib.flush(10):
                print('flushed at {}'.format(x))

        print('postloop', ib._queue)
        if ib.flush(1):
            print('post flush at {}'.format(x))

    def test_context_buffer(self):
        with InsertBuffer(self, chunksz=10) as ib:
            for x in range(101, 202):
                ib.insert1((x,))
                print(ib._queue)
                if ib.flush(10):
                    print('flushed at {}'.format(x))


if __name__ == '__main__':
    TestInsertBuffer().test()
