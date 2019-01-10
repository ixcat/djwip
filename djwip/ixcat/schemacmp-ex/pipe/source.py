
import datajoint as dj

schema = dj.schema('test_compare_source')


@schema
class FirstLevel(dj.Lookup):
    definition = '''
    id: int
    '''
    contents = [(i,) for i in range(11)]


@schema
class SecondLevel(dj.Lookup):
    definition = '''
    -> FirstLevel
    ---
    value: int
    '''
    contents = list(enumerate(range(11)))
