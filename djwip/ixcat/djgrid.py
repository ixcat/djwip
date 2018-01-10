
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
