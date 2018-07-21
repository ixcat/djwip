
import datajoint as dj

from djwip.test import CONN_INFO, PREFIX

schema = dj.schema(PREFIX + '_ixcat_chunkify', connection=dj.conn(**CONN_INFO))


@schema
class TestTable(dj.Manual):
    definition = '''
    testid:             integer         # test id
    ---
    testdat:            varchar(255)    # test data
    '''
