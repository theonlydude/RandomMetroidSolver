
from rom.rom import RealROM, snes_to_pc

def RGB_24_to_15(color_tuple):
    R_adj = int(color_tuple[0])//8
    G_adj = int(color_tuple[1])//8
    B_adj = int(color_tuple[2])//8

    c = B_adj * 1024 + G_adj * 32 + R_adj
    return (c)

def RGB_15_to_24(SNESColor):
    R = ((SNESColor      ) % 32) * 8
    G = ((SNESColor//32  ) % 32) * 8
    B = ((SNESColor//1024) % 32) * 8

    # span to 255 (limited to 248 otherwise)
    R = R + R // 32
    G = G + G // 32
    B = B + B // 32

    return (R/255.0, G/255.0, B/255.0)

def human_luminance(r, g, b):
    # color green is perceived more by human eye
    return 0.2126*r + 0.7152*g + 0.0722*b

def adjust_hue_degree(hsl_color, degree):
    hue = hsl_color[0] * 360
    hue_adj = (hue + degree) % 360

    return hue_adj/360.0

class Palette(object):
    def __init__(self, nLines=16, nColors=16):
        self.nColors = nColors
        self.nLines = nLines
        self.lines = [[(0,0,0)]*nColors for i in range(nLines)]

    @staticmethod
    def load_yychr(path, lines=list(range(16)), nColors=16):
        ret = Palette(len(lines), nColors)
        lineSize = nColors*3
        with open(path, "rb") as rgbPal:
            idx = 0
            for line in lines:
                rgbPal.seek(line*lineSize)
                for i in range(nColors):
                    colorRaw = rgbPal.read(3)
                    ret.lines[idx][i] = (int(colorRaw[0]), int(colorRaw[1]), int(colorRaw[2]))
                idx += 1
        return ret

    def save_yychr(self, path):
        with open(path, "wb") as outPal:
            for line in self.lines:
                for color in line:
                    rgb = [color[0], color[1], color[2]]
                    outPal.write(bytearray(rgb))

    @staticmethod
    def load_snes(path, offset=0, lines=list(range(16)), nColors=16):
        ret = Palette(len(lines), nColors)
        rom = RealROM(path)
        lineSize = nColors*2
        idx = 0
        for line in lines:
            rom.seek(offset + lineSize*line)
            for i in range(nColors):
                r, g, b = RGB_15_to_24(rom.readWord())
                ret.lines[idx][i] = (int(r*256), int(g*256), int(b*256))
            idx += 1
        rom.close()
        return ret

    def print_asm(self):
        for line in self.lines:
            print("    dw "+', '.join(["$%04x" % RGB_24_to_15(rgb) for rgb in line]))
