

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

    return (R/256.0, G/256.0, B/256.0)

def human_luminance(r, g, b):
    # color green is perceived more by human eye
    return 0.2126*r + 0.7152*g + 0.0722*b

def adjust_hue_degree(hsl_color, degree):
    hue = hsl_color[0] * 360
    hue_adj = (hue + degree) % 360

    return hue_adj/360.0
