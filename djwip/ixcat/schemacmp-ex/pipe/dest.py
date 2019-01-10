
import datajoint as dj

schema = dj.schema('test_compare_dest')


@schema
class FirstLevel(dj.Lookup):
    definition = '''
    id: int
    '''
    contents = [(i,) for i in range(10)]


@schema
class SecondLevel(dj.Lookup):
    definition = '''
    -> FirstLevel
    ---
    value: int
    '''
    contents = [(i, i*2 if i % 2 else i) for i in list(range(10))]
