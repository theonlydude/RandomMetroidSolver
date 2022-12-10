# store smaller palettes

def expand_palette(palette):
    out = {}
    for key, values in palette.items():
        for i, value in enumerate(values):
            out[key+i] = value
    return out

def shrink_palette(palette):
    out = {}
    old_key = -1
    i = 1
    for key, value in palette.items():
        if old_key + i == key:
            out[old_key].append(value)
            i += 1
        else:
            out[key] = [value]
            old_key = key
            i = 1
    return out
