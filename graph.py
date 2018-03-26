#!/usr/bin/python

from networkx import MultiDiGraph
from networkx.algorithms.simple_paths import all_simple_paths

#from networkx import draw_networkx
#import matplotlib.pyplot as plt

g = MultiDiGraph()

g.add_node('Crateria')
g.add_node('Green Brinstar')
g.add_node('Red Brinstar')
g.add_node('Wrecked Ship')
g.add_node('Maridia')
g.add_node('Tourian')
g.add_node('Norfair')
g.add_node('Lower Norfair')
g.add_node('Blue Brinstar')

g.add_edge('Crateria', 'Tourian')
g.add_edge('Crateria', 'Green Brinstar')
g.add_edge('Crateria', 'Wrecked Ship')
g.add_edge('Crateria', 'Red Brinstar')
g.add_edge('Crateria', 'Blue Brinstar')
g.add_edge('Green Brinstar', 'Red Brinstar')
g.add_edge('Green Brinstar', 'Blue Brinstar')
g.add_edge('Green Brinstar', 'Crateria')
g.add_edge('Blue Brinstar', 'Crateria')
g.add_edge('Blue Brinstar', 'Green Brinstar')
g.add_edge('Wrecked Ship', 'Crateria')
g.add_edge('Wrecked Ship', 'Maridia')
g.add_edge('Maridia', 'Wrecked Ship')
g.add_edge('Maridia', 'Red Brinstar')
g.add_edge('Red Brinstar', 'Green Brinstar')
g.add_edge('Red Brinstar', 'Crateria')
g.add_edge('Red Brinstar', 'Maridia')
g.add_edge('Red Brinstar', 'Norfair')
g.add_edge('Norfair', 'Red Brinstar')
g.add_edge('Norfair', 'Lower Norfair')
g.add_edge('Lower Norfair', 'Norfair')

#draw_networkx(g)
#plt.show()

for node in ['Blue Brinstar', 'Green Brinstar', 'Tourian', 'Wrecked Ship', 'Maridia', 'Red Brinstar', 'Norfair', 'Lower Norfair']:
    p = all_simple_paths(g, 'Crateria', node)
    print("Paths to {}:".format(node))
    for path in list(p):
        print("  {}".format(path))
