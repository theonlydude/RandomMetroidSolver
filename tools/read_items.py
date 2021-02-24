import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from graph.varia.graph_locations import locations as graphLocations
from rom.romloader import RomLoader

romLoader = RomLoader.factory(sys.argv[1], None)
romLoader.readNothingId()
majorsSplit = romLoader.assignItems(graphLocations)
for loc in graphLocations:
    print("{}: {}".format(loc.Name, loc.itemName))

