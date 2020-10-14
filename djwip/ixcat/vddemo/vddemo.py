#! /usr/bin/env python

from code import interact

from visidata import view_pandas as vd
import numpy as np
import datajoint as dj

schema = dj.schema('test_vddemo')


@schema
class First(dj.Manual):
    definition = '''
    first_id: int
    '''

@schema
class Second(dj.Manual):
    definition = '''
    -> First
    ---
    second_dat: longblob
    '''

def load():
    First.insert([(i,) for i in range(10)], skip_duplicates=True)
    Second.insert([dict(d, second_dat=np.array(
                   list(range(d['first_id']*10, d['first_id']*10+10))))
                   for d in First()], skip_duplicates=True)


if __name__ == '__main__':
    interact('vddemo', local=locals())


