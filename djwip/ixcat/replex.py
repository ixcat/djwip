
from code import interact
from collections import ChainMap

# not so much library code as notes; interact is called from current context
# better execution method (decorator?) possibly would make this useful.

def getscope():
    return ChainMap(locals(), globals())

def interact():
    return interact(getscope())

