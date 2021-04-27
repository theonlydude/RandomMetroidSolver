#!/usr/bin/python3
# convert inkscape svg to the one that we include in the tracker
# ./tools/gen_map_svg.py web/static/area_map.svg web/views/inc_area_map.svg

# prerequisites:
# pip3 install numpy
# pip3 install svgwrite
# pip3 install svgpathtools

import sys, os
# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

try:
    from svgpathtools import svg2paths2
except:
    print("Error: missing prerequisites")
    sys.exit(1)

srcSvg = sys.argv[1]
dstSvg = sys.argv[2]

_, attributes, _ = svg2paths2(srcSvg)

def isRect(attr):
    return 'width' in attr and 'height' in attr and 'x' in attr and 'y' in attr

def isPath(attr):
    return 'd' in attr

defaultStyle = "opacity:0.3;fill:#ffffff"
with open(dstSvg, 'w') as dstSvgFile:
    dstSvgFile.write('<!-- svg overlay test -->\n')
    dstSvgFile.write('<svg id="roomsVisibilitySvg" width="100%" height="100%" viewBox="0 0 1500 750">\n')
    for attr in attributes:
        if isPath(attr):
            dstSvgFile.write('  <path id="{}" class="svginvisible" style="{}" d="{}"/>\n'.format(attr['id'], defaultStyle, attr['d']))
        elif isRect(attr):
            dstSvgFile.write('  <rect id="{}" class="svginvisible" style="{}" width="{}" height="{}" x="{}" y="{}"/>\n'.format(attr['id']
, defaultStyle, attr['width'], attr['height'], attr['x'], attr['y']))
        else:
            print("unknown attribute: {}".format(attr))
    dstSvgFile.write('</svg>\n')

print("done")
