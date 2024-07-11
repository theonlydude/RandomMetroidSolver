#!/usr/bin/python3

import sys, os, json

mainDir = os.path.dirname(sys.path[0])
sys.path.append(mainDir)

import utils.log

from logic.logic import Logic
from rom.flavor import RomFlavor
from rom.symbols import Symbols, Freespace

flavor = "vanilla" if len(sys.argv) < 2 else sys.argv[1]

debug = False
utils.log.init(debug)

Logic.factory(flavor)
RomFlavor.factory(mainDir)

freespace = Freespace(RomFlavor.symbols)

spanWidth = lambda span: span[1]-span[0]
bankWidth = max([spanWidth(freespace.getSpan(bank)) for bank in freespace.banks])

from utils.colors import RandomColors
import pygame
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FREESPACE_COLOR = pygame.Color("antiquewhite1")
BANK_COLOR = pygame.Color("azure4")
PATCH_SCALE = 0.925
BANK_SCREEN_FONT_SIZE = 24


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

patchColors = {}
allPatches = set()

def fillPatchInfo():
    for bank, bankLayout in freespace.bankLayouts.items():
        for rg, patches in bankLayout.items():
            for p in patches:
                allPatches.add(p["patch"])
    C = lambda c: pygame.Color(int(c[0]*255), int(c[1]*255), int(c[2]*255))
    patchColorList = [C(c) for c in RandomColors.generate_random_colors(len(allPatches), pastel_factor = 0.4)]
    for patch in allPatches:
        patchColors[patch] = patchColorList.pop()

def renderBankBackground(surface, bank, bankLayout):
    w, h = surface.get_width(), surface.get_height()
    pygame.draw.rect(surface, BANK_COLOR, pygame.Rect(0, 0, w, h))
    span = freespace.getSpan(bank)
    scale = w / bankWidth
    spanStart, spanEnd = span
    yoff = int((h*(1 - PATCH_SCALE))/2)
    print(f"w = {w}, h = {h}, span = ({spanStart}, {spanEnd}), scale = {scale}, yoff = {yoff}")
    X = lambda addr: int((bankWidth - spanEnd + addr & 0xffff)*scale)
    W = lambda rg: max(spanWidth(rg)*scale, 1)
    Rpatch = lambda rg: pygame.Rect(X(rg[0]), yoff, W(rg), h - yoff*2)
    Rfree = lambda rg: pygame.Rect(X(rg[0]), 0, W(rg), h)
    for free, patches in bankLayout.items():
        r = Rfree(free)
        print(r)
        pygame.draw.rect(surface, FREESPACE_COLOR, r)
        for patch in patches:
            col = patchColors[patch["patch"]]
            for rg in patch["ranges"]:
                r = Rpatch(rg)
                print(patch, r)
                pygame.draw.rect(surface, col, r)

bankFont = pygame.font.SysFont(None, BANK_SCREEN_FONT_SIZE)
bankFontColor = pygame.Color("darkslategray")

def drawBankText(surface, bank):
    text = bankFont.render("%02X" % bank, True, (bankFontColor.r, bankFontColor.g, bankFontColor.b))
    r = text.get_rect()
    r.center = surface.get_rect().center
    surface.blit(text, r.topleft)

ROWS, COLS = 8, 7
XSTEP, YSTEP = 15, 10

assert ROWS * COLS > len(freespace.banks)

def renderBankScreen(surface, banks):
    w = int((SCREEN_WIDTH - XSTEP*(COLS + 1))/COLS)
    h = int((SCREEN_HEIGHT - YSTEP*(ROWS + 1))/ROWS)
    i = 0
    x = 0
    for c in range(COLS):
        x += XSTEP
        y = 0
        for r in range(ROWS):
            if i >= len(banks):
                return
            y += YSTEP
            surf = surface.subsurface(pygame.Rect(x, y, w, h))
            bank = banks[i]
            renderBankBackground(surf, bank, freespace.bankLayouts[bank])
            drawBankText(surf, bank)
            i += 1
            y += h
        x += w

fillPatchInfo()
renderBankScreen(screen, freespace.banks)

pygame.display.flip()

while True:
    pass
