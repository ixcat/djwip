
from qgrid import QgridWidget

import djwip.ixcat.schemax as schemax
from djwip.ixcat.pandax import DJPanda


from ipywidgets import interact_manual
from ipywidgets import IntText
from ipywidgets import FloatText
from ipywidgets import ToggleButton
from ipywidgets import Text
from ipywidgets import Textarea
from ipywidgets import DatePicker


class DJGrid:
    '''
    DataJoint/QgridWidget utility class.
    Deprecated in favor of DJRecord since we clone table state &
    dj isn't designed for data updates; possibly useful if dealing with pandas
    or updates absolutely required.
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
        return self._djpanda.save()

    def edit(self):
        # todo: get full-loop interaction going in jupyter
        #   ... using 'interact()' requires a widget with 'FIXME WHAT NEEDS'
        # basically ixgrid is a dom widget which doesn't have whatever
        # this missing note used to say.
        raise NotImplementedError(
            'edit() not implemented. Please use .display() then .save()'
        )


class DJRecord:
    '''
    DataJoint simple data entry widget.

    Needs more testing; should be functional for basic int/text cases.

    TODO:

    - longer varchar to text area dispatch
    - provide way to browse fk data records; for now, must query the foreign
      table to determine other data records and manually re-enter.

    '''

    _widgetmap = {
        'bool': (ToggleButton, {}),
        'int': (IntText, {}),
        'float': (FloatText, {}),
        'varchar': (Text, {}),
        'text': (Textarea, {}),
        'date': (DatePicker, {}),
    }

    def __init__(self, tableclass):
        self._tableclass = tableclass
        self._schema = schemax.get_schema(tableclass)
        schemax.schema_prep(self._schema)
        self._widget_dict = self._build_widget_dict()

    def _create_cb(self, **kwargs):

        print('creating with {kwargs}'.format(kwargs=str(kwargs)))
        self._tableclass().insert1(kwargs)

    def _build_widget_dict(self):
        # XXX: moar pythongish
        wd = {}
        ta = schemax.get_table_attributes(self._tableclass)
        for a in ta:
            typestr = ta[a].type.split('(')[0]
            wp = DJRecord._widgetmap[typestr]
            wd[a] = wp[0](**wp[1])

        return wd

    def create(self):
        interact_manual(self._create_cb, **self._widget_dict)
