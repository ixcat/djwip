
from djwip.ixcat.djgrid import DJGrid

if __name__ == '__main__':
    raise NotImplementedError('tests not implemented')

def doit_eventually():
    djg = DJGrid(schema, Session)
    djg.display()
    djg.save()

    try:
        djg.edit()  # display, save; need to hook to jupyter.
    except NotImplementedError:
        pass

