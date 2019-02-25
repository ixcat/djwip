import djwip.ixcat.djpatch as dj


schema = dj.schema('test_djpatch')
schema.drop(force=True)
schema = dj.schema('test_djpatch')


@schema
class DjPatchTest(dj.Manual):
    definition = '''
    patchid: int
    '''


@schema
class DjPatchAux(dj.Manual):
    definition = '''
    -> DjPatchTest
    ---
    stuff: varchar(20)
    '''


def test_djpatch():
    DjPatchTest.insert1((1,))
    DjPatchAux.insert1((1, 'aux',))

    q = {'patch_id': 1}
    print((DjPatchAux & q))
    print((DjPatchAux & q).fetch(as_dict=True))
    dj.config['safemode'] = False
    (DjPatchTest & q).delete()
    schema.drop(force=True)


if __name__ == '__main__':
    test_djpatch()
