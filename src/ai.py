from tools.getVars import loadSettings, loadTypes, dumpTypes
from tools import grab, openprocess
from errorscreen import ErrorScreen
from typescreen import TypeScreen
from time import sleep
import numpy
import mouse
import keyboard
import random
import sys


class AI:
    def __init__(self, running=None):
        if running is None:
            running = [True]
        self.running = running

        self.loadVars()
        self.loadTypes()
        self.getBox()
        self.getArr()
        self.getGrid()
        self.checkForDescreps()

        self.revealed = []
        self.outerBorderTiles = []
        self.innerBorderTiles = []
        self.compBorderConfigs = []
        self.innerExclude = []
        self.outerExclude = []
        self.emptyTiles = []

        self.clickMode = 'Collective'
        self.BF_LIMIT = 17
        self.endGame = False
        self.moves = []

        self.run()

    def loadTypes(self):
        self.types = loadTypes()

    def dumpTypes(self):
        dumpTypes(self.types)

    def loadVars(self):
        params = loadSettings()

        self.w = params["width"]
        self.h = params["height"]
        self.mineLen = params["bombs"]
        self.pw = params["pixel_width"]
        self.delay = 1 / params["fps"] * 1.04
        self.winMode = params["mode"]
        self.winTitle = params["window_name"]

        self.flags = self.mineLen

    @property
    def hasWon(self):
        self.getEmpty()
        return len(self.emptyTiles) == 0

    @property
    def open(self):
        return self.winMode == 'Fullscreen' or grab.foregroundTitle() == self.winTitle

    @property
    def emptyGrid(self):
        for i in range(self.h):
            for j in range(self.w):
                if self.grid[i][j] is not None:
                    return False
        return True

    def checkForDescreps(self):
        descrep = []
        if self.w * self.pw != self.box[2] - self.box[0]:
            descrep.append('Width and Pixel Width do not match up with window dimensions')
        if self.h * self.pw != self.box[3] - self.box[1]:
            descrep.append('Height and Pixel Height do not match up with window dimensions')
        if self.mineLen > self.w * self.h:
            descrep.append('Mine Count greater than total of Width and Height')

        if len(descrep) != 0:
            openprocess.openProcess(ErrorScreen, (descrep, ))
            self.running[0] = False
            sys.exit()

    def getType(self, y, x, init=False):
        avg = numpy.average(self.arr[y*self.pw:(y+1)*self.pw, x*self.pw:(x+1)*self.pw])

        if avg not in self.types.values():
            temp = self.types

            openprocess.openProcess(TypeScreen, (self.arr[y * self.pw:(y + 1) * self.pw, x * self.pw:(x + 1) * self.pw],))
            self.loadTypes()

            if temp == self.types:
                self.running[0] = False
                sys.exit()

        ty = list(self.types.keys())[list(self.types.values()).index(avg)]

        if ty == "Flag" and init:
            self.flags -= 1
        if ty in ["Mine", "Mineact", "WrongFlag"]:
            self.running[0] = False
            sys.exit()
        return ty

    def doMove(self, y, x, c):
        mouse.move(self.box[0] + (x + 0.5) * self.pw, self.box[1] + (y + 0.5) * self.pw)

        if c in ['r', 'l']:
            if c == 'l':
                mouse.press('left')
                sleep(self.delay)
                mouse.release('left')
            if c == 'r':
                mouse.press('right')
                sleep(self.delay)
                mouse.release('right')
        else:
            keyboard.press('space')
            sleep(self.delay)
            keyboard.release('space')

    def doMoveWithUpdate(self, y, x, c):
        self.doMove(y, x, c)

        if c == 'r':
            self.flags -= 1
            self.grid[y][x] = 'Flag'
        elif c == 's':
            self.getArr()
            for i, j in self.getSorroundingOfType(y, x, None):
                self.updateGrid(i, j)
        else:
            self.getArr()
            self.updateGrid(y, x)

    def randomMove(self):
        x, y = random.randint(0, self.w-1), random.randint(0, self.h-1)
        while self.grid[y][x] is not None:
            x, y = random.randint(0, self.w - 1), random.randint(0, self.h - 1)
        return y, x, 'l'

    def randomBorderMove(self):
        i = random.randint(0, len(self.outerBorderTiles) - 1)
        y, x = self.outerBorderTiles[i]
        while self.grid[y][x] is not None:
            i = random.randint(0, len(self.outerBorderTiles) - 1)
            y, x = self.outerBorderTiles[i]
        return y, x, 'l'

    def centerMove(self):
        return self.h//2, self.w//2, 'l'

    def updateGrid(self, i, j):
        if [i, j] not in self.revealed:
            ty = self.getType(i, j)
            if ty in range(0, 9):
                self.revealed.append([i, j])
            if self.grid[i][j] != ty:
                self.grid[i][j] = ty
                for y, x in self.getNeigh(i, j):
                    self.updateGrid(y, x)

    def getNeigh(self, i, j):
        return [[i+y, j+x] for y, x in [[1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1]] if 0 <= i+y < self.h and 0 <= j+x < self.w]

    def getSorroundingOfType(self, i, j, t):
        if type(t) in [iter, object, list, tuple, range]:
            return [[i, j] for i, j in self.getNeigh(i, j) if self.grid[i][j] in t]
        return [[i, j] for i, j in self.getNeigh(i, j) if self.grid[i][j] == t]

    def getRelated(self, i, j):
        return [[k + i, l + j] for k in range(-2, 3) for l in range(-2, 3) if [k, l] != [0, 0] and 0 <= k + i < self.h and 0 <= l + j < self.w]

    def getRelatedThatShares(self, i, j):
        for y, x in self.getRelated(i, j):
            if self.grid[y][x] in range(1, 9):
                yield [y, x]

    def getBox(self):
        box = grab.GameBoxRect()
        if not box:
            self.running[0] = False
            sys.exit()
        self.box = box[0], box[2], box[1], box[3]

    def getArr(self):
        self.arr = grab.GameBox()
        if type(self.arr) == bool:
            self.running[0] = False
            sys.exit()

    def getGrid(self):
        self.grid = [[None for j in range(self.w)] for i in range(self.h)]

        for i in range(self.h):
            for j in range(self.w):
                self.grid[i][j] = self.getType(i, j, init=True)

    def getEmpty(self):
        self.emptyTiles = []

        for i in range(self.h):
            for j in range(self.w):
                if self.grid[i][j] is None:
                    self.emptyTiles.append([i, j])

    def getFlags(self):
        flags = []

        for i in range(self.h):
            for j in range(self.w):
                if self.grid[i][j] == 'Flag':
                    flags.append([i, j])

        return flags

    def getBorder(self):
        self.outerBorderTiles = []
        self.innerBorderTiles = []

        for i in range(self.h):
            for j in range(self.w):
                if self.grid[i][j] is None:
                    s = self.getSorroundingOfType(i, j, range(1, 9))
                    if s:
                        self.outerBorderTiles.append([i, j])
                        for y, x in s:
                            if [y, x] not in self.innerBorderTiles:
                                self.innerBorderTiles.append([y, x])

    def isValid(self, bordertiles):
        """innerBorder = []

        for y, x in bordertiles:
            for i, j in self.getSorroundingOfType(y, x, range(1, 9)):
                if [i, j] not in innerBorder:
                    innerBorder.append([i, j])

        for i, j in innerBorder:
            if self.grid[i][j] != len(self.getSorroundingOfType(i, j, 'Flag')):
                return False"""

        flagLen = len(self.getFlags())

        if flagLen > self.mineLen:
            return False

        if self.endGame:
            if flagLen != self.mineLen:
                return False

        return True

    def segregateBorder(self):
        if len(self.innerBorderTiles) == 0:
            return []

        segOuter = []
        closed = []

        while len(closed) < len(self.innerBorderTiles):

            start = self.innerBorderTiles[random.randint(0, len(self.innerBorderTiles) - 1)]
            while start in closed:
                start = self.innerBorderTiles[random.randint(0, len(self.innerBorderTiles) - 1)]

            segment = []
            innerSegment = [start]
            self.recurseSegregate(*start, segment, innerSegment)

            closed += innerSegment
            segOuter.append(segment)

        return segOuter

    def recurseSegregate(self, i, j, r, s):
        for k, l in self.getRelatedThatShares(i, j):
            if [k, l] not in s:
                for n, m in self.getSorroundingOfType(k, l, None):
                    if [n, m] not in r:
                        r.append([n, m])

                s.append([k, l])
                self.recurseSegregate(k, l, r, s)

    def simpleProbability(self, segment):
        lst = []

        for i, j, in segment:
            pos = []

            for y, x in self.getSorroundingOfType(i, j, range(1, 9)):
                chance = (self.grid[y][x] - len(self.getSorroundingOfType(y, x, 'Flag'))) / len(self.getSorroundingOfType(y, x, None))
                pos.append(chance)

            if len(pos) == 0:
                lst.append(len(self.emptyTiles) / (self.mineLen - len(self.getFlags())))

            else:
                lst.append(max(pos))

        return lst

    def probabilityMove(self):
        self.getEmpty()
        chanceArr = []

        if len(self.outerBorderTiles) == 0:
            if len(self.emptyTiles):
                self.doMove(*self.randomMove())
            return

        self.endGame = False

        if len(self.emptyTiles) < self.BF_LIMIT:
            segOuterBorder = [self.emptyTiles]
            self.outerBorderTiles = self.emptyTiles
            self.endGame = True

        elif len(self.outerBorderTiles) < self.BF_LIMIT:
            segOuterBorder = [self.outerBorderTiles]

        else:
            segOuterBorder = self.segregateBorder()
            self.outerBorderTiles = [b for a in segOuterBorder for b in a]

        for segment in segOuterBorder:
            if len(segment) < self.BF_LIMIT:
                self.compBorderConfigs = []
                self.getCompatibleConfigs(segment, [])

                if len(self.compBorderConfigs) == 0:
                    chanceArr += [0.5 for _ in range(len(segment))]
                    continue

                for i in range(len(self.compBorderConfigs[0])):
                    c = 0
                    for j in range(len(self.compBorderConfigs)):
                        if self.compBorderConfigs[j][i]:
                            c += 1
                    chanceArr.append(c / len(self.compBorderConfigs))

            else:
                chanceArr += self.simpleProbability(segment)

        if len(chanceArr) != len(self.outerBorderTiles):
            self.doMove(*self.randomBorderMove())
            return

        s = False
        for i in range(len(chanceArr)):

            if chanceArr[i] == 0.0:
                self.doMove(self.outerBorderTiles[i][0], self.outerBorderTiles[i][1], 'l')
                s = True

            elif chanceArr[i] == 1.0:
                self.doMove(self.outerBorderTiles[i][0], self.outerBorderTiles[i][1], 'l')
                s = True

        if s:
            return

        i = chanceArr.index(min(chanceArr))
        y, x = self.outerBorderTiles[i]
        self.doMove(y, x, 'l')

    def getCompatibleConfigs(self, bordertiles, arr, k=0):
        for i, j in self.innerBorderTiles:
            numFlags = len(self.getSorroundingOfType(i, j, 'Flag'))

            if numFlags > self.grid[i][j]:
                return

            if all(point in bordertiles[:k] for point in self.getSorroundingOfType(i, j, None)):
                if numFlags != self.grid[i][j]:
                    return

        if k >= len(bordertiles):
            if self.isValid(bordertiles):
                self.compBorderConfigs.append(arr[:])
            return

        arr.append(True)
        self.grid[bordertiles[k][0]][bordertiles[k][1]] = 'Flag'
        self.getCompatibleConfigs(bordertiles, arr, k+1)
        arr.pop(k)
        self.grid[bordertiles[k][0]][bordertiles[k][1]] = None

        arr.append(False)
        self.grid[bordertiles[k][0]][bordertiles[k][1]] = None
        self.getCompatibleConfigs(bordertiles, arr, k+1)
        arr.pop(k)
        self.grid[bordertiles[k][0]][bordertiles[k][1]] = None

    def simpleMovesCollective(self):
        self.innerExclude = []
        self.outerExclude = []
        self.getBorder()

        for i, j in self.innerBorderTiles:
            if [i, j] not in self.innerExclude:
                if len(self.getSorroundingOfType(i, j, None)) != 0:
                    if self.grid[i][j] == len(self.getSorroundingOfType(i, j, None)) + len(self.getSorroundingOfType(i, j, 'Flag')):
                        for y, x in self.getSorroundingOfType(i, j, None):
                            if [y, x] not in self.outerExclude:
                                self.moves.append((y, x, 'r'))
                                self.outerExclude.append([y, x])
                        self.innerExclude.append([i, j])

        for i, j in self.innerBorderTiles:
            if [i, j] not in self.innerExclude:
                if self.grid[i][j] == len(self.getSorroundingOfType(i, j, 'Flag')):
                    if len(self.getSorroundingOfType(i, j, None)) == 0:
                        for y, x in self.getSorroundingOfType(i, j, None):
                            if [y, x] not in self.outerExclude:
                                self.outerExclude.append([y, x])
                        self.moves.append((i, j, 's'))
                        self.innerExclude.append([i, j])

        if len(self.moves) == 0:
            for i, j in self.innerBorderTiles:
                if [i, j] not in self.innerExclude:
                    for y, x in [[y, x] for y, x in self.getRelated(i, j) if self.grid[y][x] in range(1, 9)]:
                        a = self.getSorroundingOfType(y, x, None)
                        b = self.getSorroundingOfType(i, j, None)
                        shared = [point for point in a if point in b]
                        if self.grid[y][x] - len(self.getSorroundingOfType(y, x, 'Flag')) - (len(a) - len(shared)) == \
                            self.grid[i][j] - len(self.getSorroundingOfType(i, j, 'Flag')):
                            for k, l in [point for point in b if point not in a]:
                                if [k, l] not in self.outerExclude:
                                    self.moves.append((k, l, 'l'))
                                    self.outerExclude.append([k, l])

            for i, j in self.innerBorderTiles:
                if [i, j] not in self.innerExclude:
                    for y, x in [[y, x] for y, x in self.getRelated(i, j) if self.grid[y][x] in range(1, 9)]:
                        a = self.getSorroundingOfType(y, x, None)
                        b = self.getSorroundingOfType(i, j, None)
                        shared = [point for point in a if point in b]
                        if self.grid[i][j] - len(self.getSorroundingOfType(i, j, 'Flag')) > self.grid[y][x] - len(self.getSorroundingOfType(y, x, 'Flag')):
                            if (self.grid[i][j] - len(self.getSorroundingOfType(i, j, 'Flag'))) - (self.grid[y][x] - len(self.getSorroundingOfType(y, x, 'Flag'))) == len(b) - len(shared):
                                for k, l in [point for point in b if point not in a]:
                                    if [k, l] not in self.outerExclude:
                                        self.moves.append((k, l, 'r'))
                                        self.outerExclude.append([k, l])

        self.moves = list(dict.fromkeys(self.moves))

    def simpleMoves(self):
        temp = [list(row) for row in self.grid]

        self.getBorder()
        for i, j in self.innerBorderTiles:
            if self.grid[i][j] == len(self.getSorroundingOfType(i, j, None)) + len(self.getSorroundingOfType(i, j, 'Flag')):
                for y, x in self.getNeigh(i, j):
                    if self.grid[y][x] is None:
                        self.doMoveWithUpdate(y, x, 'r')

        self.getBorder()
        for i, j in self.innerBorderTiles:
            if self.grid[i][j] == len(self.getSorroundingOfType(i, j, 'Flag')):
                if len(self.getSorroundingOfType(i, j, None)) == 0:
                    self.doMoveWithUpdate(i, j, 's')

        self.getBorder()
        for i, j in self.innerBorderTiles:
            for y, x in [[y, x] for y, x in self.getRelated(i, j) if self.grid[y][x] in range(1, 9)]:
                a = self.getSorroundingOfType(y, x, None)
                b = self.getSorroundingOfType(i, j, None)
                shared = [point for point in a if point in b]
                if self.grid[y][x] - len(self.getSorroundingOfType(y, x, 'Flag')) - len(a) + len(shared) == self.grid[i][j] - len(self.getSorroundingOfType(i, j, 'Flag')):
                    for k, l in [point for point in b if point not in a]:
                        self.doMoveWithUpdate(k, l, 'l')

        self.getBorder()
        for i, j in self.innerBorderTiles:
            for y, x in [[y, x] for y, x in self.getRelated(i, j) if self.grid[y][x] in range(1, 9)]:
                a = self.getSorroundingOfType(y, x, None)
                b = self.getSorroundingOfType(i, j, None)
                shared = [point for point in a if point in b]
                if self.grid[i][j] - len(self.getSorroundingOfType(i, j, 'Flag')) > self.grid[y][x] - len(self.getSorroundingOfType(y, x, 'Flag')):
                    if (self.grid[i][j] - len(self.getSorroundingOfType(i, j, 'Flag'))) - (self.grid[y][x] - len(self.getSorroundingOfType(y, x, 'Flag'))) == len(b) - len(shared):
                        for k, l in [point for point in b if point not in a]:
                            self.doMoveWithUpdate(k, l, 'r')

        if temp == self.grid:
            return True
        return False

    def wait(self):
        while True:
            if self.open:
                self.getBox()
                self.getArr()
                self.checkForDescreps()
                self.getGrid()
                return
            sleep(1)

    def run(self):
        if self.emptyGrid:
            self.doMove(*self.centerMove())
            sleep(self.delay)
        self.solve()

    def solve(self):
        while self.open and not self.hasWon:
            self.getArr()
            self.getGrid()
            self.getBorder()

            if self.clickMode == 'Collective':
                self.simpleMovesCollective()

                if not self.moves:
                    self.probabilityMove()

                else:
                    for move in self.moves:
                        self.doMove(*move)

                    self.moves = []

            else:

                if self.simpleMoves():
                    self.probabilityMove()

        self.running[0] = False
