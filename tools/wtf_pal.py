
import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rando.sprite_palettes import sprite_palettes
from rando.palettes import palettes

pal_off = [1123742, 889856, 890912, 890944, 890976, 891008, 891040, 891072, 891104, 891136, 891680, 891712, 891744, 891776, 891808, 891840, 891872, 891904, 891936, 891968, 892000, 892032, 892064, 892096, 892128, 892160, 449387, 449466, 449545, 449624, 449700, 451686, 451720, 451754, 451788, 451822, 451856, 451890, 451924, 451958, 451992, 452026, 452060, 452094, 452128, 452162, 452196, 449423, 449581, 449660, 449502, 890144, 891168, 891200, 891232, 891264, 891296, 891328, 891360, 891392, 892192, 892224, 892256, 892288, 892320, 892352, 892384, 892416, 892448, 892480, 892512, 892544, 892576, 892608, 892640, 892672, 449745, 449824, 449903, 449982, 450058, 452242, 452276, 452310, 452344, 452378, 452412, 452446, 452480, 452514, 452548, 452582, 452616, 452650, 452684, 452718, 452752, 449781, 449860, 449939, 450018, 890176, 890208, 890240, 890272, 890304, 890336, 890368, 890400, 890432, 890464, 890496, 890528, 890752, 890784, 890816, 890848, 890880, 891424, 891456, 891488, 891520, 891552, 891584, 891616, 891648, 892704, 892736, 892768, 892800, 892832, 892864, 892896, 892928, 892960, 892992, 893024, 893056, 893088, 893120, 893152, 893184, 450103, 450182, 450261, 450340, 450416, 452798, 452832, 452866, 452900, 452934, 452968, 453002, 453036, 453070, 453104, 453138, 453172, 453206, 453240, 453274, 453308, 450139, 450218, 450297, 450376]
sz = 0x0F
samus = sprite_palettes['samus.ips']
vanilla = palettes.copy()

def readWord(d, off):
    w0 = d[off]
    w1 = d[off+1]
    w = (w1 << 8) + w0
    return w

assert len(pal_off) == len(set(pal_off))

def pal_cmp():
    with open("samus.csv", "w") as f:
        f.write("Address,Vanilla,Custom_Samus,Difference\n")
        for base_off in pal_off:
            for off in range(0, sz + 1):
                if off == 4:
                    continue
                addr = base_off + (off * 2)
                ws = readWord(samus, addr)
                wv = readWord(vanilla, addr)
                f.write("0x%x,0x%x,0x%x,%d\n" % (addr,wv,ws,abs(wv-ws)))
    #            assert wv == ws, "offset 0x%x : colors differ. v = 0x%x, s = 0x%x" % (addr, wv, ws)
    #            print "addr 0x%x OK !" % addr
    #        print "addr 0x%x OK !" % base_off


#pal_cmp()
def power_up():
    addrs = [ 0xd9400, 0xd9402, 0xd9404, 0xd9406, 0xd940a, 0xd940c, 0xd940e, 0xd9410, 0xd9412, 0xd9414, 0xd9416, 0xd9418, 0xd941a, 0xd941c, 0xd941e ]
    for a in addrs:
        assert(vanilla[a] == palettes[a] and vanilla[a] == samus[a])
    vanilla.update(samus)
    for a in addrs:
        assert(vanilla[a] == palettes[a] and vanilla[a] == samus[a])

power_up()

