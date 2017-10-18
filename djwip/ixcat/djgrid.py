
from qgrid import QgridWidget

from djwip.ixcat.pandax import DJPanda


# todo: provide 'interact' method to use with DJGrid
# https://ipywidgets.readthedocs.io/en/latest/examples/Using%20Interact.html


class DJGrid:
    '''
    DataJoint/QgridWidget utility class.
    '''
    def __init__(self, schema, tableclass):
        self._djpanda = DJPanda(schema, tableclass)
        self._widget = None

    def display(self):
        df = self._djpanda.fetch()
        self._widget = QgridWidget(df=df, show_toolbar=True)
        return self._widget

    def save(self):
        self._djpanda._edit = self._widget.get_changed_df()
        self._djpanda.save()

    def edit(self):
        # todo: get full-loop interaction going in jupyter
        raise NotImplementedError(
            'edit() not implemented. Please use .display() then .save()'
        )
