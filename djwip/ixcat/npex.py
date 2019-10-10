
import numpy as np

def dct2rec(dat):
    ''' 
    convert list-of-dict to numpy recarray
    type handling is admittedly hackish..
    '''
    return np.rec.array([tuple(i.values()) for i in dat],
                        np.dtype[(k, type(v)) for k, v in dat[0].items()])

