from tools.getVars import loadSettings, loadTypes, dumpTypes
from tools import grab, openprocess
from errorscreen import ErrorScreen
from typescreen import TypeScreen
from time import sleep
import numpy
import random
import sys
from pynput import mouse, keyboard


class Solver:
    def __init__(self, running=None):
        if running is None:
            running = [True]
        self.running = running

        self.typesTable = {
            't': ['tile'],
            'i': ['0', '1', '2', '3', '4', '5', '6', '7', '8'],
            'f': ['flag'],
            'm': ['mine', 'activated_mine']
        }

        self.box = grab.gameBoxRect()
        if not self.box:
            self.running[0] = False
            sys.exit()

        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()
        self.loadVars()
        self.loadTypes()

        self.checkForDescreps()

        self.grid = [['tile' for j in range(self.w)] for i in range(self.h)]
        self.typeDetectionApprox = 0.01
        self.updateGrid()

        self.outerBorderTiles = []
        self.innerBorderTiles = []
        self.compBorderConfigs = []

        self.BF_LIMIT = 17
        self.endGame = False

        self.run()

    def parseInputProfile(self, obj):
        if obj["device"] == "mouse":
            key = mouse.__dict__[obj["type"]].__dict__[obj["key"]]

            return lambda: (
                self.mouse_controller.press(key),
                sleep(self.delay),
                self.mouse_controller.release(key)
            )

        else:
            if obj["type"] == "Key":
                key = keyboard.Key.__dict__[obj["key"]]
            else:
                key = keyboard.KeyCode(char=obj["key"])

            return lambda: (
                self.mouse_controller.press(mouse.Button.left),
                self.mouse_controller.release(mouse.Button.left),
                self.keyboard_controller.press(key),
                sleep(self.delay),
                self.keyboard_controller.release(key)
            )


    def loadTypes(self):
        self.types = loadTypes()
        self.typesValues = list(self.types.values())
        self.typesKeys = list(self.types.keys())

    def dumpTypes(self):
        dumpTypes(self.types)

    def loadVars(self):
        params = loadSettings()

        self.w = params["width"]
        self.h = params["height"]
        self.mineLen = params["bombs"]
        self.pw = (self.box[1] - self.box[0]) // self.w
        self.delay = 1 / params["fps"] * 1.04
        self.reveal_field = self.parseInputProfile(params["reveal_field"])
        self.place_flag = self.parseInputProfile(params["place_flag"])
        self.reveal_neigh = self.parseInputProfile(params["reveal_neigh"])
        self.winMode = params["mode"]
        self.winTitle = params["window_name"]

    @property
    def windowOpen(self):
        return self.winMode == 'Fullscreen' or grab.foregroundTitle() == self.winTitle

    @property
    def emptyGrid(self):
        for i in range(self.h):
            for j in range(self.w):
                if self.grid[i][j] != 'tile':
                    return False

        return True

    @property
    def fullGrid(self):
        for i in range(self.h):
            for j in range(self.w):
                if self.grid[i][j] == 'tile':
                    return False

        return True

    def find(self, t):
        content = self.typesTable[t]
        matches = []

        for i in range(self.h):
            for j in range(self.w):
                if self.grid[i][j] in content:
                    matches.append([i, j])

        return matches

    def findLen(self, t):
        content = self.typesTable[t]
        c = 0

        for i in range(self.h):
            for j in range(self.w):
                if self.grid[i][j] in content:
                    c += 1

        return c

    def neighbors(self, i, j):
        return [[i+y, j+x] for y, x in [[1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1]] if 0 <= i+y < self.h and 0 <= j+x < self.w]

    def sorroundingFind(self, i, j, t):
        content = self.typesTable[t]
        return [[y, x] for y, x in self.neighbors(i, j) if self.grid[y][x] in content]

    def sorroundingFindLen(self, i, j, t):
        content = self.typesTable[t]
        c = 0

        for y, x in self.neighbors(i, j):
            if self.grid[y][x] in content:
                c += 1

        return c

    def getSharingBorderPoint(self, i, j):
        related = []

        for y, x in self.sorroundingFind(i, j, 't'):
            for n, m in self.sorroundingFind(y, x, 'i'):
                if n != i or m != j:
                    related.append([n, m])

        return related

    def getSharingBorderPointLen(self, i, j):
        c = 0

        for y, x in self.sorroundingFind(i, j, 't'):
            for n, m in self.sorroundingFind(y, x, 'i'):
                if n != i or m != j:
                    c += 1

        return c

    def checkForDescreps(self):
        descrep = []
        if self.w * self.pw != self.box[1] - self.box[0]:
            descrep.append('Width and Pixel Width do not match up with window dimensions')
        if self.h * self.pw != self.box[3] - self.box[2]:
            descrep.append('Height and Pixel Height do not match up with window dimensions')
        if self.mineLen > self.w * self.h:
            descrep.append('Mine Count greater than total of Width and Height')

        if len(descrep) != 0:
            openprocess.openProcess(ErrorScreen, (descrep, ))
            self.running[0] = False
            sys.exit()

    def updateGrid(self):
        self.arr = grab.gameBox()
        if type(self.arr) == bool:
            self.running[0] = False
            sys.exit()

        for i in range(self.h):
            for j in range(self.w):
                self.grid[i][j] = self.readType(i, j)

    def updateBorder(self):
        self.outerBorderTiles = []
        self.innerBorderTiles = []

        for i, j in self.find('i'):
            sorroundingTiles = self.sorroundingFind(i, j, 't')
            if sorroundingTiles:
                self.innerBorderTiles.append([i, j])
                for y, x in sorroundingTiles:
                    if [y, x] not in self.outerBorderTiles:
                        self.outerBorderTiles.append([y, x])

    def readType(self, y, x):
        avg = numpy.average(self.arr[y*self.pw:(y+1)*self.pw, x*self.pw:(x+1)*self.pw])
        match = None

        for typeValue in self.typesValues:
            if abs(avg - typeValue) < self.typeDetectionApprox:
                match = typeValue
                break

        if match is None:
            temp = self.types

            openprocess.openProcess(TypeScreen, (self.arr[y * self.pw:(y + 1) * self.pw, x * self.pw:(x + 1) * self.pw],))
            self.loadTypes()

            if temp == self.types:
                self.running[0] = False
                sys.exit()

            for typeValue in self.typesValues:
                if abs(avg - typeValue) < self.typeDetectionApprox:
                    match = typeValue
                    break

        ty = self.typesKeys[self.typesValues.index(match)]

        if ty in ["mine", "activated_mine", "incorrect_flag"]:
            self.running[0] = False
            sys.exit()
        return ty

    def doMove(self, y, x, c):
        self.mouse_controller.position = self.box[0] + (x + 0.5) * self.pw, self.box[2] + (y + 0.5) * self.pw

        if c == 'reveal_field':
            self.reveal_field()
        elif c == 'place_flag':
            self.place_flag()
        elif c == "reveal_neigh":
            self.reveal_neigh()

    def randomMove(self):
        x, y = random.randint(0, self.w-1), random.randint(0, self.h-1)
        while self.grid[y][x] != 'tile':
            x, y = random.randint(0, self.w - 1), random.randint(0, self.h - 1)
        return y, x, 'reveal_field'

    def randomBorderMove(self):
        i = random.randint(0, len(self.outerBorderTiles) - 1)
        y, x = self.outerBorderTiles[i]
        while self.grid[y][x] != 'tile':
            i = random.randint(0, len(self.outerBorderTiles) - 1)
            y, x = self.outerBorderTiles[i]
        return y, x, 'reveal_field'

    def centerMove(self):
        return self.h//2, self.w//2, 'reveal_field'

    def getCompatibleConfigs(self, bordertiles, arr, k=0):
        for i, j in self.innerBorderTiles:
            numFlags = self.sorroundingFindLen(i, j, 'f')

            if numFlags > int(self.grid[i][j]):
                return

            if all(point in bordertiles[:k] for point in self.sorroundingFind(i, j, 't')):
                if numFlags != int(self.grid[i][j]):
                    return

        if k >= len(bordertiles):
            flagLen = self.findLen('f')

            if not flagLen > self.mineLen:
                if not self.endGame or flagLen == self.mineLen:
                    self.compBorderConfigs.append(arr[:])
            return

        arr.append(True)
        self.grid[bordertiles[k][0]][bordertiles[k][1]] = 'flag'
        self.getCompatibleConfigs(bordertiles, arr, k+1)
        arr.pop(k)
        self.grid[bordertiles[k][0]][bordertiles[k][1]] = 'tile'

        arr.append(False)
        self.grid[bordertiles[k][0]][bordertiles[k][1]] = 'tile'
        self.getCompatibleConfigs(bordertiles, arr, k+1)
        arr.pop(k)
        self.grid[bordertiles[k][0]][bordertiles[k][1]] = 'tile'

    def segregateBorder(self):
        if len(self.innerBorderTiles) == 0:
            return []

        segOuter = []
        closed = []

        while len(closed) < len(self.innerBorderTiles):

            start = self.innerBorderTiles[random.randint(0, len(self.innerBorderTiles) - 1)]
            while start in closed:
                start = self.innerBorderTiles[random.randint(0, len(self.innerBorderTiles) - 1)]

            segment = self.sorroundingFind(*start, 't')
            innerSegment = [start]
            self.recurseSegregate(*start, segment, innerSegment)

            closed += innerSegment
            segOuter.append(segment)

        return segOuter

    def recurseSegregate(self, i, j, r, s):
        for k, l in self.getSharingBorderPoint(i, j):
            if [k, l] not in s:
                for n, m in self.sorroundingFind(k, l, 't'):
                    if [n, m] not in r:
                        r.append([n, m])

                s.append([k, l])
                self.recurseSegregate(k, l, r, s)

    def simpleProbability(self, segment):
        lst = []

        for i, j, in segment:
            pos = []

            for y, x in self.sorroundingFind(i, j, 'i'):
                chance = (int(self.grid[y][x]) - self.sorroundingFindLen(y, x, 'f')) / self.sorroundingFindLen(y, x, 't')
                pos.append(chance)

            if len(pos) == 0:
                lst.append((self.mineLen - self.findLen('f')) / self.findLen('t'))

            else:
                lst.append(max(pos))

        return lst

    def probabilityMove(self):
        emptyTiles = self.find('t')
        chanceArr = []

        if len(self.outerBorderTiles) == 0:
            if len(emptyTiles):
                self.doMove(*self.randomMove())
            return

        self.endGame = False

        if len(emptyTiles) < self.BF_LIMIT:
            segOuterBorder = [emptyTiles]
            self.outerBorderTiles = emptyTiles
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
                self.doMove(self.outerBorderTiles[i][0], self.outerBorderTiles[i][1], 'reveal_field')
                s = True

            elif chanceArr[i] == 1.0:
                self.doMove(self.outerBorderTiles[i][0], self.outerBorderTiles[i][1], 'place_flag')
                s = True

        if s:
            return

        i = chanceArr.index(min(chanceArr))
        y, x = self.outerBorderTiles[i]
        self.doMove(y, x, 'reveal_field')

    def simpleMoves(self):
        for i, j in self.innerBorderTiles:

            pointNum = int(self.grid[i][j])
            sorroundingTiles = self.sorroundingFind(i, j, 't')
            sorroundingFlagsLen = self.sorroundingFindLen(i, j, 'f')

            if pointNum == len(sorroundingTiles) + sorroundingFlagsLen:
                for y, x in sorroundingTiles:
                    yield y, x, 'place_flag'

        for i, j in self.innerBorderTiles:

            pointNum = int(self.grid[i][j])
            sorroundingFlagsLen = self.sorroundingFindLen(i, j, 'f')

            if pointNum == sorroundingFlagsLen:
                yield i, j, 'reveal_neigh'

        for i, j in self.innerBorderTiles:

            sharingPoints = self.getSharingBorderPoint(i, j)
            sourceSorroundingTiles = self.sorroundingFind(i, j, 't')
            sourceSorroundingFlags = self.sorroundingFind(i, j, 'f')
            sourceNum = int(self.grid[i][j])

            for y, x in sharingPoints:

                targetSorroundingTiles = self.sorroundingFind(y, x, 't')
                targetSorroundingFlagsLen = self.sorroundingFindLen(y, x, 'f')
                targetNum = int(self.grid[y][x])

                sharedSorroundingTiles = [point for point in targetSorroundingTiles if point in sourceSorroundingTiles]
                sourceExclusiveSorroundingTiles = [point for point in sourceSorroundingTiles if point not in targetSorroundingTiles]

                if targetNum - targetSorroundingFlagsLen - (len(targetSorroundingTiles) - len(sharedSorroundingTiles)) == sourceNum - len(sourceSorroundingFlags):
                    for k, l in sourceExclusiveSorroundingTiles:
                        yield k, l, 'reveal_field'

        for i, j in self.innerBorderTiles:

            sharingPoints = self.getSharingBorderPoint(i, j)
            sourceSorroundingTiles = self.sorroundingFind(i, j, 't')
            sourceSorroundingFlagsLen = self.sorroundingFindLen(i, j, 'f')
            sourceNum = int(self.grid[i][j])

            for y, x in sharingPoints:
                targetSorroundingTiles = self.sorroundingFind(y, x, 't')
                targetSorroundingFlagsLen = self.sorroundingFindLen(y, x, 'f')
                targetNum = int(self.grid[y][x])

                sharedSorroundingTiles = [point for point in targetSorroundingTiles if point in sourceSorroundingTiles]
                sourceExclusiveSorroundingTiles = [point for point in sourceSorroundingTiles if point not in targetSorroundingTiles]

                if sourceNum - sourceSorroundingFlagsLen > targetNum - targetSorroundingFlagsLen:
                    if (sourceNum - sourceSorroundingFlagsLen) - (targetNum - targetSorroundingFlagsLen) == len(sourceSorroundingTiles) - len(sharedSorroundingTiles):
                        for k, l in sourceExclusiveSorroundingTiles:
                            yield k, l, 'place_flag'

    def wait(self):
        while True:
            if self.windowOpen:
                self.checkForDescreps()
                self.updateGrid()
                return
            sleep(1)

    def run(self):
        if self.emptyGrid:
            self.doMove(*self.centerMove())
            sleep(self.delay)
        self.solve()

    def solve(self):
        while self.windowOpen and not self.fullGrid:
            self.updateGrid()
            self.updateBorder()

            moves = self.simpleMoves()

            already_done = []
            for move in moves:
                if move not in already_done:
                    already_done.append(move)
                    self.doMove(*move)

            if not already_done:
                self.probabilityMove()

        self.running[0] = False

if __name__ == '__main__':
    Solver()
