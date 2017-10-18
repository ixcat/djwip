

import pandas as pd

from djwip.ixcat.schemax import schema_prep, get_table_attributes


def table2df(table, fetch=True):
    ''' fetch a UserRelation as a DataFrame '''
    columns = [k for k in get_table_attributes(table)]
    data = table().fetch() if fetch else []
    return pd.DataFrame(data=data, columns=columns)


def df_append(df, tuplist):
    ''' return dataframe contaning result of appending tuplist to df '''
    return df.append(
        pd.DataFrame(data=tuplist, columns=df.columns),
        ignore_index=True)


def df_append1(df, tup):
    ''' return dataframe contaning result of appending tup to df '''
    return df_append(df, list(tup))


def df_diff(olddf, newdf):
    '''
    Return a dataframe consisting of the members of newdf not in old df.
    Original index values will be lost due to reindexing.
    TODO: Cover more than only 'additional items' case.
    '''
    ret = pd.DataFrame(data=[], columns=newdf.columns)
    subset = newdf.index.isin(list(set(newdf.index) - set(olddf.index)))
    return ret.append(newdf[subset], ignore_index=True)


def df_iter(df):
    ''' generate index iterator over dataframe '''
    return (df.iloc[i].tolist() for i in df.index)


def df_save(tableclass, olddf, newdf):
    ''' save dataframe differences to table '''
    # XXX: 'differences' defined by dfdiff, which only supports additions atm
    tableclass().insert(df_iter(df_diff(olddf, newdf)))


class DJPanda:
    '''
    DataJoint to Pandas Table wrapper gizmo

    Currently as thin layer around procedural methods designed for data
    editing.

    Basically just keeps track of 2 data frames: '_edit' and '_orig'.
    The '_edit' is frame is the current working copy,
    and '_orig' is either an empty frame matching the schema or
    the table contents.

    The dfsave method will calculate the difference via procedural dfsave,

    a data frame which is either empty or the current table contents,
    and use dfsave to save the differences in '_edit' when called.
    '''
    def __init__(self, schema, tableclass):
        ''' Construct a DJPanda from the given schema and tableclass '''
        schema_prep(schema)
        self._table = tableclass
        self._orig = None
        self._edit = None
        self.clear()

    def clear(self):
        ''' clear the dataframe associated with this DJPanda '''
        self._edit = self._orig = table2df(self._table, fetch=False)
        return self._edit

    def _rebase(self):
        ''' set baseline to current edit '''
        self._orig = self._edit
        return self._edit

    def fetch(self):
        ''' fetch database values into this DJPanda '''
        self.clear()
        self.append(self._table().fetch())
        return self._rebase()

    def append(self, tuplist):
        ''' append a list of tuples to the current edit '''
        self._edit = df_append(self._edit, tuplist)
        return self._edit

    def append1(self, tup):
        ''' append a tuple to the current edit '''
        return self.append(list(tup))

    def save(self):
        ''' save the current edit '''
        df_save(self._table, self._orig, self._edit)
        return self._rebase()
