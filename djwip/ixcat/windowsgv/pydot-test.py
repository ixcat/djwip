# todo: doit.
import pydot

# via
# https://github.com/erocarrera/pydot/blob/master/test/pydot_unittest.py
import pydot

g = pydot.Dot()
g.set_type('digraph')

node = pydot.Node('legend')
node.set("shape", 'box')
g.add_node(node)
node.set('label', 'mine')
s = g.to_string()
s_0 = 'digraph G {\nlegend [label=mine, shape=box];\n}\n'
s_1 = 'digraph G {\nlegend [shape=box, label=mine];\n}\n'
assert s == s_0 or s == s_1, (s, s_0)

print('\n'.join((n for n in g.__dict__.keys() if 'write_' in n)))
print(*(n for n in g.__dict__.keys() if 'write_' in n), sep='\n')



g = pydot.Graph()
s = pydot.Subgraph("foo")
g.add_subgraph(s)
g.add_edge( pydot.Edge('A','B') )
g.add_edge( pydot.Edge('A','C') )
g.add_edge( pydot.Edge( ('D','E') ) )
g.add_node( pydot.Node( 'node!' ) )

# pydot has saving hmm..
# how to view in jupyter..
from IPython.display import Image
Image(g.create_png())


''' networkx via pydot '''

import networkx as nx
G = nx.Graph()
G.add_edge('A', 'B', weight=4)
G.add_edge('B', 'D', weight=2)
G.add_edge('A', 'C', weight=3)
G.add_edge('C', 'D', weight=4)

# networkx future gotcha: 
# 1.x works w/pydotplus, 2.x works w/pydot 

import pydotplus
Image(nx.nx_pydot.to_pydot(G).create_png())
