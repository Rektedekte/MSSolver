from tools.uielements import drawtxt
from tools.window import Window
from tools.grab import GameBoxImg
from tools import getVars
import pygame

pw = 3


class OffsetManager(Window):
    def __init__(self, running=None):
        if running is None:
            running = [True]
        self.running = running

        vars = getVars.loadSettings()

        self.mode = vars["mode"]
        self.windowName = vars["window_name"]

        self.img = GameBoxImg(o=False)

        if not self.img:
            self.running[0] = False
            return

        super().__init__(*self.img.get_size(), 'GameBox Manager')

        self.move(0, 0)
        if self.mode == 'Window':
            self.restore()
        self.displayWidth, self.displayHeight = self.win.get_size()

        self.font = pygame.font.Font('fonts/OpenSans-ExtraBold.ttf', 30)

        self.box = Box(self.displayWidth, self.displayHeight, getVars.loadOffset())

        self.focus = None
        self.pw = 3

        self.run()

    def apply(self):
        getVars.dumpOffset(self.box.offset)

    def snapToSide(self, x, y):
        disToLeft = abs(x - self.box.left)
        disToRight = abs(x - self.box.right)
        disToTop = abs(y - self.box.top)
        disToBottom = abs(y - self.box.bottom)

        low = disToLeft
        self.focus = 'left'
        if disToRight < low:
            low = disToRight
            self.focus = 'right'
        if disToTop < low:
            low = disToTop
            self.focus = 'top'
        if disToBottom < low:
            self.focus = 'bottom'

    def unSnapToSide(self):
        self.focus = None

    def adjustSideToPos(self, x, y):
        if self.focus == 'left':
            if x >= self.box.right:
                self.box.left = self.box.right
            else:
                self.box.left = x
        elif self.focus == 'right':
            if x <= self.box.left:
                self.box.right = self.box.left
            else:
                self.box.right = x
        elif self.focus == 'top':
            if y >= self.box.bottom:
                self.box.top = self.box.bottom
            else:
                self.box.top = y
        else:
            if y <= self.box.top:
                self.box.bottom = self.box.top
            else:
                self.box.bottom = y

    def draw(self):
        self.win.blit(self.img, (0, 0))

        pygame.draw.rect(self.win, (0, 255, 0), self.box.rect, pw)

        drawtxt('Width: {}'.format(self.box.width), self.font, (0, 255, 0), (self.displayWidth * 0.003, self.displayHeight * 0.02), 'l', self.win)
        drawtxt('Height: {}'.format(self.box.height), self.font, (0, 255, 0), (self.displayWidth * 0.003, self.displayHeight * 0.05), 'l', self.win)

        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running[0] = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.apply()
                    if event.key == pygame.K_ESCAPE:
                        self.running[0] = False
                        return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    self.snapToSide(x, y)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.unSnapToSide()

            if self.focus:
                self.adjustSideToPos(*pygame.mouse.get_pos())

            self.draw()
            self.clock.tick(24)


class Box:
    def __init__(self, disWidth, disHeight, offset):
        self.disWidth = disWidth
        self.disHeight = disHeight

        self.left = offset[0]
        self.right = disWidth - offset[1]
        self.top = offset[2]
        self.bottom = disHeight - offset[3]

        if not self.isValid():
            self.left = 0
            self.right = disWidth
            self.top = 0
            self.bottom = disHeight

    @property
    def rect(self):
        return self.left - pw + 1, self.top - pw + 1, self.width + pw * 2 - 2, self.height + pw * 2 - 2

    @property
    def offset(self):
        return [self.offsetL, self.offsetR, self.offsetT, self.offsetB]

    @property
    def offsetL(self):
        return self.left

    @property
    def offsetR(self):
        return self.disWidth - self.right

    @property
    def offsetT(self):
        return self.top

    @property
    def offsetB(self):
        return self.disHeight - self.bottom

    @property
    def width(self):
        return self.disWidth - self.offsetL - self.offsetR

    @property
    def height(self):
        return self.disHeight - self.offsetT - self.offsetB

    def isValid(self):
        return self.right >= self.left and self.bottom >= self.top
