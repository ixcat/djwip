#! /usr/bin/env python

from code import interact

from pipe import source
from pipe import dest

schemas = [source, dest]
tablenames = ['FirstLevel', 'SecondLevel']
tablepairs = {t: (getattr(source, t), getattr(dest, t)) for t in tablenames}


def show(comment=''):
    print('# {} table contents'.format(comment))
    for p in tablepairs:
        print(p)
        for t in tablepairs[p]:
            print(t)
            print(t())


def push():
    try:
        print('# pushing data')
        for tname in tablenames:
            source_tbl, dest_tbl = tablepairs[tname]
            dest_tbl.insert(source_tbl() - dest_tbl().proj())
    except Exception as e:
        print('# push error: {e}'.format(e=e))


def diff():
    print('# diff')
    ndiff = 0
    for t in tablenames:
        a, b = tablepairs[t]

        for i in ((a - b.proj()).fetch('KEY')):
            print('# {} only in {} - record deleted?'.format(i, a))

        for i in ((b - a.proj()).fetch('KEY')):
            print('# {} only in {} - record deleted?'.format(i, b))

        common = (a & b.proj())
        kstr = ', '.join(a.primary_key)
        srcrecs = (a & common.proj()).fetch(order_by=kstr, as_dict=True)
        dstrecs = (b & common.proj()).fetch(order_by=kstr, as_dict=True)

        for srce, dste in zip(srcrecs, dstrecs):
            print('# comparing key: {}'.format(
                [srce[i] for i in a.primary_key]))

            for attr in srce:
                srcv = srce[attr]
                dstv = dste[attr]
                if srcv != dstv:
                    print('# {t}.{a}: {s} != {d}'.format(
                        t=t, a=attr, s=srcv, d=dstv))
                    ndiff += 1

        print('# {} total differences.'.format(ndiff))

    return ndiff


def drop():
    for s in schemas:
        s.schema.drop(force=True)


if __name__ == '__main__':
    show('initial')
    print('pre-diff')
    diff()
    push()
    show('post-diff')
    diff()
    show('resulting')
    interact('do-compare shell', local=locals())
