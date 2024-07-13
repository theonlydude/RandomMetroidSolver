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
BANK_VIEWER_WSCALE = 0.9
BANK_VIEWER_HSCALE = 0.25

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

def renderBankBackground(surface, bank, bankLayout, freeOnly=False):
    w, h = surface.get_width(), surface.get_height()
    pygame.draw.rect(surface, BANK_COLOR, surface.get_rect())
    span = freespace.getSpan(bank)
    width = bankWidth if not freeOnly else spanWidth(span)
    scale = w / width
    spanStart, spanEnd = span
    yoff = int((h*(1 - PATCH_SCALE))/2)
#    print(f"w = {w}, h = {h}, span = ({spanStart}, {spanEnd}), scale = {scale}, yoff = {yoff}")
    X = lambda addr: int((width - spanEnd + addr & 0xffff)*scale)
    W = lambda rg: max(spanWidth(rg)*scale, 1)
    Rpatch = lambda rg: pygame.Rect(X(rg[0]), yoff, W(rg), h - yoff*2)
    Rfree = lambda rg: pygame.Rect(X(rg[0]), 0, W(rg), h)
    for free, patches in bankLayout.items():
        r = Rfree(free)
#        print(r)
        pygame.draw.rect(surface, FREESPACE_COLOR, r)
        for patch in patches:
            col = patchColors[patch["patch"]]
            for rg in patch["ranges"]:
                r = Rpatch(rg)
#                print(patch, r)
                pygame.draw.rect(surface, col, r)

bankFont = pygame.font.SysFont(None, BANK_SCREEN_FONT_SIZE)
bankFontColor = pygame.Color("darkslategray")

def drawBankText(surface, bank):
    text = bankFont.render("%02X" % bank, True, bankFontColor)
    r = text.get_rect()
    r.center = surface.get_rect().center
    surface.blit(text, r.topleft)

ROWS, COLS = 8, 7
XSTEP, YSTEP = 15, 10

OVERVIEW_BANK_WIDTH = int((SCREEN_WIDTH - XSTEP*(COLS + 1))/COLS)
OVERVIEW_BANK_HEIGHT = int((SCREEN_HEIGHT - YSTEP*(ROWS + 1))/ROWS)
OVERVIEW_XMAX = (OVERVIEW_BANK_WIDTH + XSTEP)*COLS
OVERVIEW_YMAX = (OVERVIEW_BANK_HEIGHT + YSTEP)*ROWS

assert ROWS * COLS >= len(freespace.banks)

fillPatchInfo()

class Mode(object):
    current = None

    def clicked(self, clickPos):
        print(f"clicked! {clickPos}")

    def mouseMoved(self, mousePos):
        pass
        #print(f'Mouse moved to {mousePos}')

    def draw(self):
        screen.fill((0, 0, 0))
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update(self):
        pass

class BankOverview(Mode):
    def __init__(self):
        self._isInsideBank = False

    def clicked(self, clickPos):
        super().clicked(clickPos)
        bank = self.findBank(clickPos)
        if bank is not None:
            Mode.current = BankViewer(bank)

    def mouseMoved(self, mousePos):
        super().mouseMoved(mousePos)
        isInside = self.isInsideBank(mousePos)
        if isInside != self._isInsideBank:
            cursor = pygame.SYSTEM_CURSOR_HAND if isInside else pygame.SYSTEM_CURSOR_ARROW
            pygame.mouse.set_cursor(cursor)
            self._isInsideBank = isInside

    def draw(self):
        super().draw()
        self.renderBankScreen(screen, freespace.banks)

    def renderBankScreen(self, surface, banks):
        w = OVERVIEW_BANK_WIDTH
        h = OVERVIEW_BANK_HEIGHT
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
                print(f"{bank:x}: c={c}, r={r} : xmin = {x}, xmax = {x+w}, ymin={y}, ymax={y+h}")
                renderBankBackground(surf, bank, freespace.bankLayouts[bank])
                drawBankText(surf, bank)
                i += 1
                y += h
            x += w

    def isInsideBank(self, pos):
        x, y = pos
        w, h = OVERVIEW_BANK_WIDTH + XSTEP, OVERVIEW_BANK_HEIGHT + YSTEP
        ret = x < OVERVIEW_XMAX and y < OVERVIEW_YMAX and x % w > XSTEP and y % h > YSTEP
        if ret and x > w * (COLS - 1): # last column
            ret = y / h < len(freespace.banks) % ROWS
    #    print(f"isInsideBank: ({x % w}, {y % h}, {w}, {h})? {ret}")
        return ret

    def findBank(self, pos):
        if not self.isInsideBank(pos):
            return None
        x, y = pos
        w, h = OVERVIEW_BANK_WIDTH + XSTEP, OVERVIEW_BANK_HEIGHT + YSTEP
        c, r = int(x / w), int(y / h)
        bank = freespace.banks[c * ROWS + r]
        print(f"found bank: {bank:x}")
        return bank

overview = BankOverview()

class BankViewer(Mode):
    def __init__(self, bank):
        self._bank = bank

    def draw(self):
        super().draw()
        rect = screen.get_rect().scale_by(BANK_VIEWER_WSCALE, BANK_VIEWER_HSCALE)
        rect.center = screen.get_rect().center
        surf = screen.subsurface(rect)
        renderBankBackground(surf, self._bank, freespace.bankLayouts[self._bank], freeOnly=True)

    def clicked(self, clickPos):
        Mode.current = overview

def mainLoop():
    prevMode = None
    Mode.current = overview
    while True:
        if prevMode != Mode.current:
            print("draw mode")
            Mode.current.draw()
            prevMode = Mode.current
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                # click released
                Mode.current.clicked(clickPos)
            elif event.type == pygame.MOUSEMOTION:
                Mode.current.mouseMoved(event.pos)
        Mode.current.update()
        pygame.display.flip()

mainLoop()
