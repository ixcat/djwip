# true wip to patch dj
# immediate goal: hooking queries, query logging, query tuning
# long-run goal: make this modular or find appropriate library
#  perhaps: https://gorilla.readthedocs.io/en/latest/tutorial.html
# usage:
# import djpatch as dj

import sys

import datajoint as dj

djpatch = sys.modules[__name__]
dj_vars = vars(dj)

#
# patched functions
#


def query(self, query, args=(), as_dict=False, suppress_warnings=True,
          reconnect=None):
    print('patched query', query)
    return self.djpatch_query(query, args, as_dict, suppress_warnings,
                              reconnect)

#
# patch installation / 'main'
#

dj_vars['Connection'].djpatch_query = dj_vars['Connection'].query
dj_vars['Connection'].query = query

for a in dj.__all__:
    setattr(djpatch, a, dj_vars[a])

__all__ = dj.__all__
