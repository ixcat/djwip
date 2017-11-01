
from qgrid import QgridWidget

import djwip.ixcat.schemax as schemax
from djwip.ixcat.pandax import DJPanda


from ipywidgets import interact_manual
from ipywidgets import IntText
from ipywidgets import FloatText
from ipywidgets import ToggleButton
from ipywidgets import Text
from ipywidgets import Textarea

'''
Note:
DatePicker not so supported, so using text input for now.

# from ipywidgets import DatePicker

/ipywidgets/docs/source/examples/Widget%20List.ipynb:

  "The date picker widget works in Chrome and IE Edge, but does not currently
  work in Firefox or Safari because they do not support the HTML date input
  field."

https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/date#Browser_compatibility

Will be fixed in next FF release (57), still nothing in Opera.
'''


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
    - provide way to browse fk data records; for now, must query the foreign
      table to determine other data records and manually re-enter.
    '''

    _widgetmap = {
        'bool': (ToggleButton, {}),             # XXX: not dj supported
        'tinyint': (IntText, {}),               # TODO: limit max input?
        'tinyint unsigned': (IntText, {}),      # TODO: >0; limit max?
        'smallint': (IntText, {}),              # TODO: limit max input?
        'smallint unsigned': (IntText, {}),     # TODO: >0; limit max?
        'mediumint': (IntText, {}),             # TODO: limit max input?
        'mediumint unsigned': (IntText, {}),    # TODO: >0; limit max?
        'int': (IntText, {}),                   # TODO: limit max input?
        'int unsigned': (IntText, {}),          # TODO: >0; limit max?
        'enum': (Text, {}),                     # TODO: choices -> dropdown
        'date': (Text, {}),                     # TODO: comment fmt?
        'time': (Text, {}),                     # TODO: comment fmt?
        'timestamp': (Text, {}),                # TODO: comment fmt?
        'char': (Text, {}),                     # TODO: length, Textarea
        'varchar': (Text, {}),                  # TODO: length, Textarea
        'float': (FloatText, {}),               # TODO: limit max?
        'double': (FloatText, {}),              # TODO: limit max?
        'decimal': (FloatText, {}),             # TODO: test, parse fixlen
        'decimal unsigned': (FloatText, {}),    # TODO: test, parse, fixlen

        # TODO: file upload support for blobs..
        # see also:

        # https://github.com/jupyter-widgets/ipywidgets/issues/1542
        # https://github.com/peteut/ipython-file-upload

        # tinyblob
        # mediumblob
        # blob
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


def create(tableclass):
    ''' convenience wrapper around DJRecord '''
    DJRecord(tableclass).create()
