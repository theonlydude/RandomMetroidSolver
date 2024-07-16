#!/usr/bin/python3

import sys, os, json

mainDir = os.path.dirname(sys.path[0])
sys.path.append(mainDir)

import utils.log

from logic.logic import Logic
from rom.flavor import RomFlavor
from rom.symbols import Symbols, Freespace
from collections import namedtuple

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
PATCH_SCALE = 0.9
BANK_SCREEN_FONT_SIZE = 24
BANK_VIEWER_TITLE_FONT_SIZE = 48
PATCH_INFO_FONT_SIZE = 32
BANK_VIEWER_WSCALE = 0.95
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

Region = namedtuple("Region", ["rect", "range", "patch"])

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
    ret = { "free": [], "patches": []}
    for free, patches in bankLayout.items():
        r = Rfree(free)
#        print(r)
        pygame.draw.rect(surface, FREESPACE_COLOR, r)
        ret["free"].append(Region(r, free, None))
        for patch in patches:
            col = patchColors[patch["patch"]]
            for rg in patch["ranges"]:
                r = Rpatch(rg)
#                print(patch, r)
                pygame.draw.rect(surface, col, r)
                ret["patches"].append(Region(r, rg, patch["patch"]))
    # add free space sections between patches
    ret["patches"].sort(key=lambda region: region.range[0])
    freeSections = []
    for i, region in enumerate(ret["patches"]):
        current = region.range
        previous = ret["patches"][i - 1].range
        if i == 0 and current[0] != span[0]:
            free = (span[0], current[0] - 1)
            freeSections.append(Region(Rpatch(free), free, None))
        if i > 0 and current[0] - previous[1] > 2:
            free = (previous[1] + 1, current[0] - 1)
            freeSections.append(Region(Rpatch(free), free, None))
        if i == len(ret["patches"]) - 1 and current[1] != span[1]:
            free = (current[1] + 1, span[1])
            freeSections.append(Region(Rpatch(free), free, None))
    ret["patches"] += freeSections
    return ret

bankFont = pygame.font.SysFont(None, BANK_SCREEN_FONT_SIZE)
bankFontColor = pygame.Color("darkslategray")

bankTitleFont = pygame.font.SysFont(None, BANK_VIEWER_TITLE_FONT_SIZE)
bankTitleFontColor = pygame.Color("antiquewhite1")

patchInfoFont = pygame.font.SysFont(None, PATCH_INFO_FONT_SIZE)
patchInfoFontColor = pygame.Color("darkolivegreen1")

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
#                print(f"{bank:x}: c={c}, r={r} : xmin = {x}, xmax = {x+w}, ymin={y}, ymax={y+h}")
                renderBankBackground(surf, bank, freespace.bankLayouts[bank])
                self.drawBankText(surf, bank)
                i += 1
                y += h
            x += w

    def drawBankText(self, surface, bank):
        text = bankFont.render("%02X" % bank, True, bankFontColor)
        r = text.get_rect()
        r.center = surface.get_rect().center
        surface.blit(text, r.topleft)

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
        self._bankRect = screen.get_rect().scale_by(BANK_VIEWER_WSCALE, BANK_VIEWER_HSCALE)
        self._bankRect.center = screen.get_rect().center
        self._displayedRegion = None
        self._patchInfoArea = None
        self._regions = None

    def draw(self):
        super().draw()
        text = bankTitleFont.render("BANK %02X" % self._bank, True, bankTitleFontColor)
        r = text.get_rect()
        r.centerx = screen.get_rect().centerx
        r.y = 2 * YSTEP
        screen.blit(text, r.topleft)
        self._patchInfoArea = pygame.Rect(0, r.bottom + 1, screen.get_width(), self._bankRect.top - 1 - r.bottom)
        surf = screen.subsurface(self._bankRect)
        self._regions = renderBankBackground(surf, self._bank, freespace.bankLayouts[self._bank], freeOnly=True)

    def clicked(self, clickPos):
        super().clicked(clickPos)
        if not self._bankRect.collidepoint(clickPos):
            Mode.current = overview

    def mouseMoved(self, mousePos):
        super().mouseMoved(mousePos)
        if not self._bankRect.collidepoint(mousePos):
            self._clearText()
            self._displayedRegion = None
            return
        region = self._findRegion(mousePos)
        if region != self._displayedRegion:
#            print(f"switch region to {region}")
            self._clearText()
            self._displayedRegion = region
            if region is not None:
                self._showRegionText(region)

    def _clearText(self):
        pygame.draw.rect(screen, (0, 0, 0), self._patchInfoArea)

    def _findRegion(self, pos):
        x, y = pos
        x -= self._bankRect.left
        y -= self._bankRect.top
        def findRegion(regionList):
            nonlocal x, y
            return next((region for region in regionList if region.rect.collidepoint((x, y))), None)
        ret = findRegion(self._regions["patches"])
        if ret is None:
            ret = findRegion(self._regions["free"])
        return ret

    def _showRegionText(self, region):
        regionName = region.patch if region.patch is not None else "Free Space"
        size = spanWidth(region.range) + 1
        start, end = region.range
        y = self._patchInfoArea.top + 2 * YSTEP
        def showText(txt):
            nonlocal y
            text = patchInfoFont.render(txt, True, patchInfoFontColor)
            r = text.get_rect()
            r.x = 2 * XSTEP
            r.y = y
            screen.blit(text, r.topleft)
            y = r.bottom + 2 * YSTEP
        showText(regionName)
        showText("%d bytes" % size)
        showText("[$%06x, $%06x]" % (start, end))

def mainLoop():
    prevMode = None
    Mode.current = overview
    while True:
        if prevMode != Mode.current:
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
