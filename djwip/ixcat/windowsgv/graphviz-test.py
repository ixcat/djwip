
# coding: utf-8

# In[1]:


import platform

print(
    platform.system(),
    platform.version(),
    platform.machine(),
    platform.node(),
    platform.python_compiler(),
    platform.python_implementation(),
    platform.python_version(),
    platform.python_revision(),
)


# In[2]:


from graphviz import Source, Digraph

dot = Digraph(comment='The Round Table')

dot

dot.node('A', 'King Arthur')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')

dot.edges(['AB', 'AL'])
dot.edge('B', 'L', constraint='false')

print(dot.source)



# In[3]:


Source(dot)


# In[4]:


# saves file, spawns viewer
# dot.render('test-output/round-table.gv', view=True)

