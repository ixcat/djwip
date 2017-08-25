
'''
ixcat.csvex: simple wrappers around core csv for k:v data reading
'''

import csv


class CSVBase(object):
    '''
    Base CSV Class - handles basic csv file read ops

    :param fname: name of file to open

    Remaining *args / **kwargs are passed to csv.reader
    '''
    def __init__(self, fname, *args, **kwargs):
        self.reader = csv.reader(open(fname, 'r'), *args, **kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        return self.reader.__next__()


class CSVColumnDict(CSVBase):
    '''
    Like CSVBase, but uses csv.DictReader to return dicts per file headings.

    :param fname: name of file to open

    Remaining *args / **kwargs are passed to csv.DictReader
    '''
    def __init__(self, fname, *args, **kwargs):
        self.reader = csv.DictReader(open(fname, 'r'), *args, **kwargs)


class CSVRowDict(CSVBase):
    '''
    CSV Class for 'K,V' CSV files
    (e.g. file where each row contains a key and value pair of a single record)

    :param fname: name of file to open
    :param heading: whether the file has a heading line (will be ignored)

    Remaining *args / **kwargs are passed to csv.DictReader
    '''
    def __init__(self, fname, heading=False, *args, **kwargs):
        super().__init__(fname, *args, **kwargs)
        self.heading = heading
        self.dct = None

    def __next__(self):
        try:
            tups = [(k, v) for k, v in self.reader]
            if self.heading:
                return(dict(tups[1:]))
            else:
                return(dict(tups))
        except StopIteration:
            raise

    def get(self):
        if self.dct is None:
            self.dct = next(self)
        return self.dct
