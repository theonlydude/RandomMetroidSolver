#!/usr/bin/python

from networkx import MultiDiGraph
from networkx.algorithms.simple_paths import all_simple_paths

#from networkx import draw_networkx
#import matplotlib.pyplot as plt

g = MultiDiGraph()

# Crateria and Blue Brinstar
g.add_node('Crateria Landing Site')
g.add_node('Crateria Lower Mushrooms')
g.add_node('Crateria Moat')
g.add_node('Crateria Keyhunter Room')
g.add_node('Blue Brinstar Morph Ball Room')

g.add_edge('Crateria Landing Site', 'Crateria Lower Mushrooms' )
g.add_edge('Crateria Landing Site', 'Crateria Moat')
g.add_edge('Crateria Landing Site', 'Crateria Keyhunter Room')
g.add_edge('Crateria Landing Site', 'Blue Brinstar Morph Ball Room')
g.add_edge('Crateria Lower Mushrooms', 'Crateria Moat')
g.add_edge('Crateria Lower Mushrooms', 'Crateria Keyhunter Room')
g.add_edge('Crateria Lower Mushrooms', 'Blue Brinstar Morph Ball Room')
g.add_edge('Crateria Moat', 'Crateria Lower Mushrooms')
g.add_edge('Crateria Moat', 'Crateria Keyhunter Room')
g.add_edge('Crateria Moat', 'Blue Brinstar Morph Ball Room')
g.add_edge('Crateria Keyhunter Room', 'Crateria Lower Mushrooms')
g.add_edge('Crateria Keyhunter Room', 'Crateria Moat')
g.add_edge('Crateria Keyhunter Room', 'Blue Brinstar Morph Ball Room')
g.add_edge('Blue Brinstar Morph Ball Room', 'Crateria Lower Mushrooms')
g.add_edge('Blue Brinstar Morph Ball Room', 'Crateria Moat')
g.add_edge('Blue Brinstar Morph Ball Room', 'Crateria Keyhunter Room')

# Green and Pink Brinstar
g.add_node('Green Pink Brinstar Elevator')
g.add_node('Green Pink Brinstar Green Hill Zone')
g.add_node('Green Pink Brinstar Noob Bridge')

g.add_edge('Green Pink Brinstar Elevator', 'Green Pink Brinstar Green Hill Zone')
g.add_edge('Green Pink Brinstar Elevator', 'Green Pink Brinstar Noob Bridge')
g.add_edge('Green Pink Brinstar Green Hill Zone', 'Green Pink Brinstar Elevator')
g.add_edge('Green Pink Brinstar Green Hill Zone', 'Green Pink Brinstar Noob Bridge')
g.add_edge('Green Pink Brinstar Noob Bridge', 'Green Pink Brinstar Elevator')
g.add_edge('Green Pink Brinstar Noob Bridge', 'Green Pink Brinstar Green Hill Zone')

# Wrecked Ship
g.add_node('Wrecked Ship West Ocean')
g.add_node('Wrecked Ship Crab Maze')

g.add_edge('Wrecked Ship West Ocean', 'Wrecked Ship Crab Maze')
g.add_edge('Wrecked Ship Crab Maze', 'Wrecked Ship West Ocean')

# Lower Norfair
g.add_node('Lower Norfair Lava Dive')
g.add_node('Lower Norfair Three Muskateers Room')

g.add_edge('Lower Norfair Lava Dive', 'Lower Norfair Three Muskateers Room')
g.add_edge('Lower Norfair Three Muskateers Room', 'Lower Norfair Lava Dive')

# Norfair
g.add_node('Norfair Warehouse Entrance')
g.add_node('Norfair Single Chamber')
g.add_node('Norfair Kronic Boost Room')

g.add_edge('Norfair Warehouse Entrance', 'Norfair Single Chamber')
g.add_edge('Norfair Warehouse Entrance', 'Norfair Kronic Boost Room')
g.add_edge('Norfair Single Chamber', 'Norfair Warehouse Entrance')
g.add_edge('Norfair Single Chamber', 'Norfair Kronic Boost Room')
g.add_edge('Norfair Kronic Boost Room', 'Norfair Warehouse Entrance')
g.add_edge('Norfair Kronic Boost Room', 'Norfair Single Chamber')

# Maridia
g.add_node('Maridia Main Street')
g.add_node('Maridia Red Fish Room')
g.add_node('Maridia Crab Hole')
g.add_node('Maridia Coude')

g.add_edge('Maridia Main Street', 'Maridia Red Fish Room')
g.add_edge('Maridia Main Street', 'Maridia Crab Hole')
g.add_edge('Maridia Main Street', 'Maridia Coude')
g.add_edge('Maridia Red Fish Room', 'Maridia Main Street')
g.add_edge('Maridia Red Fish Room', 'Maridia Crab Hole')
g.add_edge('Maridia Red Fish Room', 'Maridia Coude')
g.add_edge('Maridia Crab Hole', 'Maridia Main Street')
g.add_edge('Maridia Crab Hole', 'Maridia Red Fish Room')
g.add_edge('Maridia Crab Hole', 'Maridia Coude')
g.add_edge('Maridia Coude', 'Maridia Main Street')
g.add_edge('Maridia Coude', 'Maridia Red Fish Room')
g.add_edge('Maridia Coude', 'Maridia Crab Hole')

# Red Brinstar
g.add_node('Red Brinstar Red Tower')
g.add_node('Red Brinstar Caterpillar Room')
g.add_node('Red Brinstar East Tunnel Down')
g.add_node('Red Brinstar East Tunnel Up')
g.add_node('Red Brinstar Glass Tunnel')
g.add_node('Red Brinstar Elevator to Red Brinstar')

g.add_edge('Red Brinstar Red Tower', 'Red Brinstar Caterpillar Room')
g.add_edge('Red Brinstar Red Tower', 'Red Brinstar East Tunnel Down')
g.add_edge('Red Brinstar Red Tower', 'Red Brinstar East Tunnel Up')
g.add_edge('Red Brinstar Red Tower', 'Red Brinstar Glass Tunnel')
g.add_edge('Red Brinstar Red Tower', 'Red Brinstar Elevator to Red Brinstar')
g.add_edge('Red Brinstar Caterpillar Room', 'Red Brinstar Red Tower')
g.add_edge('Red Brinstar Caterpillar Room', 'Red Brinstar East Tunnel Down')
g.add_edge('Red Brinstar Caterpillar Room', 'Red Brinstar East Tunnel Up')
g.add_edge('Red Brinstar Caterpillar Room', 'Red Brinstar Glass Tunnel')
g.add_edge('Red Brinstar Caterpillar Room', 'Red Brinstar Elevator to Red Brinstar')
g.add_edge('Red Brinstar East Tunnel Down', 'Red Brinstar Red Tower')
g.add_edge('Red Brinstar East Tunnel Down', 'Red Brinstar Caterpillar Room')
g.add_edge('Red Brinstar East Tunnel Down', 'Red Brinstar East Tunnel Up')
g.add_edge('Red Brinstar East Tunnel Down', 'Red Brinstar Glass Tunnel')
g.add_edge('Red Brinstar East Tunnel Down', 'Red Brinstar Elevator to Red Brinstar')
g.add_edge('Red Brinstar East Tunnel Up', 'Red Brinstar Red Tower')
g.add_edge('Red Brinstar East Tunnel Up', 'Red Brinstar Caterpillar Room')
g.add_edge('Red Brinstar East Tunnel Up', 'Red Brinstar East Tunnel Down')
g.add_edge('Red Brinstar East Tunnel Up', 'Red Brinstar Glass Tunnel')
g.add_edge('Red Brinstar East Tunnel Up', 'Red Brinstar Elevator to Red Brinstar')
g.add_edge('Red Brinstar Glass Tunnel', 'Red Brinstar Red Tower')
g.add_edge('Red Brinstar Glass Tunnel', 'Red Brinstar Caterpillar Room')
g.add_edge('Red Brinstar Glass Tunnel', 'Red Brinstar East Tunnel Down')
g.add_edge('Red Brinstar Glass Tunnel', 'Red Brinstar East Tunnel Up')
g.add_edge('Red Brinstar Glass Tunnel', 'Red Brinstar Elevator to Red Brinstar')
g.add_edge('Red Brinstar Elevator to Red Brinstar', 'Red Brinstar Red Tower')
g.add_edge('Red Brinstar Elevator to Red Brinstar', 'Red Brinstar Caterpillar Room')
g.add_edge('Red Brinstar Elevator to Red Brinstar', 'Red Brinstar East Tunnel Down')
g.add_edge('Red Brinstar Elevator to Red Brinstar', 'Red Brinstar East Tunnel Up')
g.add_edge('Red Brinstar Elevator to Red Brinstar', 'Red Brinstar Glass Tunnel')

# add vanilla transitions
g.add_edge('Crateria Lower Mushrooms', 'Green Pink Brinstar Elevator')
g.add_edge('Green Pink Brinstar Elevator', 'Crateria Lower Mushrooms')
g.add_edge('Blue Brinstar Morph Ball Room', 'Green Pink Brinstar Green Hill Zone')
g.add_edge('Green Pink Brinstar Green Hill Zone', 'Blue Brinstar Morph Ball Room')
g.add_edge('Crateria Moat', 'Wrecked Ship West Ocean')
g.add_edge('Wrecked Ship West Ocean', 'Crateria Moat')
g.add_edge('Crateria Keyhunter Room', 'Red Brinstar Elevator to Red Brinstar')
g.add_edge('Red Brinstar Elevator to Red Brinstar', 'Crateria Keyhunter Room')
g.add_edge('Green Pink Brinstar Noob Bridge', 'Red Brinstar Red Tower')
g.add_edge('Red Brinstar Red Tower', 'Green Pink Brinstar Noob Bridge')
g.add_edge('Wrecked Ship Crab Maze', 'Maridia Coude')
g.add_edge('Maridia Coude', 'Wrecked Ship Crab Maze')
g.add_edge('Norfair Kronic Boost Room', 'Lower Norfair Lava Dive')
g.add_edge('Lower Norfair Lava Dive', 'Norfair Kronic Boost Room')
g.add_edge('Lower Norfair Three Muskateers Room', 'Norfair Single Chamber')
g.add_edge('Norfair Single Chamber', 'Lower Norfair Three Muskateers Room')
g.add_edge('Norfair Warehouse Entrance', 'Red Brinstar East Tunnel Down')
g.add_edge('Red Brinstar East Tunnel Down', 'Norfair Warehouse Entrance')
g.add_edge('Red Brinstar East Tunnel Up', 'Maridia Crab Hole')
g.add_edge('Maridia Crab Hole', 'Red Brinstar East Tunnel Up')
g.add_edge('Red Brinstar Caterpillar Room', 'Maridia Red Fish Room')
g.add_edge('Maridia Red Fish Room', 'Red Brinstar Caterpillar Room')
g.add_edge('Red Brinstar Glass Tunnel', 'Maridia Main Street')
g.add_edge('Maridia Main Street', 'Red Brinstar Glass Tunnel')

#draw_networkx(g)
#plt.show()

#for node in ['Crateria Lower Mushrooms', 'Crateria Moat', 'Crateria Keyhunter Room', 'Blue Brinstar Morph Ball Room', 'Green Pink Brinstar Elevator', 'Green Pink Brinstar Green Hill Zone', 'Green Pink Brinstar Noob Bridge', 'Wrecked Ship West Ocean', 'Wrecked Ship Crab Maze', 'Lower Norfair Lava Dive', 'Lower Norfair Three Muskateers Room', 'Norfair Warehouse Entrance', 'Norfair Single Chamber', 'Norfair Kronic Boost Room', 'Maridia Main Street', 'Maridia Red Fish Room', 'Maridia Crab Hole', 'Maridia Coude', 'Red Brinstar Red Tower', 'Red Brinstar Caterpillar Room', 'Red Brinstar East Tunnel Down', 'Red Brinstar East Tunnel Up', 'Red Brinstar Glass Tunnel', 'Red Brinstar Elevator to Red Brinstar']:
#    p = all_simple_paths(g, 'Crateria Landing Site', node)
#    print("Paths to {}: {}".format(node, len(list(p))))
    #for path in list(p):
    #    print("  {}".format(path))


s = MultiDiGraph()

s.add_node('Crateria')
s.add_node('Green Pink Brinstar')
s.add_node('Red Brinstar')
s.add_node('Wrecked Ship')
s.add_node('Maridia')
s.add_node('Tourian')
s.add_node('Norfair')
s.add_node('Lower Norfair')
s.add_node('Blue Brinstar')

s.add_edge('Crateria', 'Tourian')
s.add_edge('Crateria', 'Green Brinstar')
s.add_edge('Crateria', 'Wrecked Ship')
s.add_edge('Crateria', 'Red Brinstar')
s.add_edge('Crateria', 'Blue Brinstar')
s.add_edge('Green Pink Brinstar', 'Red Brinstar')
s.add_edge('Green Pink Brinstar', 'Blue Brinstar')
s.add_edge('Green Pink Brinstar', 'Crateria')
s.add_edge('Blue Brinstar', 'Crateria')
s.add_edge('Blue Brinstar', 'Green Pink Brinstar')
s.add_edge('Wrecked Ship', 'Crateria')
s.add_edge('Wrecked Ship', 'Maridia')
s.add_edge('Maridia', 'Wrecked Ship')
s.add_edge('Maridia', 'Red Brinstar')
s.add_edge('Red Brinstar', 'Green Pink Brinstar')
s.add_edge('Red Brinstar', 'Crateria')
s.add_edge('Red Brinstar', 'Maridia')
s.add_edge('Red Brinstar', 'Norfair')
s.add_edge('Norfair', 'Red Brinstar')
s.add_edge('Norfair', 'Lower Norfair')
s.add_edge('Lower Norfair', 'Norfair')


for node in ['Blue Brinstar', 'Green Pink Brinstar', 'Tourian', 'Wrecked Ship', 'Maridia', 'Red Brinstar', 'Norfair', 'Lower Norfair']:
    p = all_simple_paths(s, 'Crateria', node)
    print("Paths to {}:".format(node))
    for path in list(p):
        print("  {}".format(path))
