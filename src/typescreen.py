from tools.window import Window
from tools.uielements import Button, TextField
from tools.getVars import loadTypes, dumpTypes, dumpImage
from numpy import average
import pygame
import sys


class TypeScreen(Window):
    def __init__(self, img, running=None, testing=False):
        if running is None:
            running = [True]
        self.running = running
        self.testing = testing

        super().__init__(450, 400, 'What is this?')

        self.avg = average(img)
        self.arr = img
        self.img = pygame.pixelcopy.make_surface(img[::-1])
        self.img = pygame.transform.rotate(self.img, 90)
        self.img = pygame.transform.scale(self.img, (100, 100))

        self.imgRect = pygame.Rect(self.w * 0.5, self.h * 0.4, *self.img.get_size())
        self.imgRect.center = (self.imgRect.x, self.imgRect.y)

        self.titleFont = pygame.font.Font('fonts/OpenSans-SemiBold.ttf', 40)
        self.subFont = pygame.font.Font('fonts/OpenSans-Light.ttf', 20)

        self.title = TextField('What is this?', (self.w * 0.5, self.h * 0.1), self.titleFont, 'c')
        self.createButtons()

        self.focus = None

        self.run()

    def createButtons(self):
        self.buttons = []
        s = self.w / 5
        self.none = Button('None', (s * 0, self.h * 0.6, s, self.h * 0.2), None, self.subFont, (240, 240, 240))
        self.flag = Button('Flag', (s * 1, self.h * 0.6, s, self.h * 0.2), 'Flag', self.subFont, (240, 240, 240))
        self.mine = Button('Mine', (s * 2, self.h * 0.6, s, self.h * 0.2), 'Mine', self.subFont, (240, 240, 240))
        self.mineAct = Button('MineA', (s * 3, self.h * 0.6, s, self.h * 0.2), 'Mineact', self.subFont, (240, 240, 240))
        self.wrongFlag = Button('WrongF', (s * 4, self.h * 0.6, s, self.h * 0.2), 'WrongFlag', self.subFont, (240, 240, 240))
        s = self.w / 9
        self.zero = Button('0', (s * 0, self.h * 0.8, s, self.h * 0.2), 0, self.subFont, (240, 240, 240))
        self.one = Button('1', (s * 1, self.h * 0.8, s, self.h * 0.2), 1, self.subFont, (240, 240, 240))
        self.two = Button('2', (s * 2, self.h * 0.8, s, self.h * 0.2), 2, self.subFont, (240, 240, 240))
        self.three = Button('3', (s * 3, self.h * 0.8, s, self.h * 0.2), 3, self.subFont, (240, 240, 240))
        self.four = Button('4', (s * 4, self.h * 0.8, s, self.h * 0.2), 4, self.subFont, (240, 240, 240))
        self.five = Button('5', (s * 5, self.h * 0.8, s, self.h * 0.2), 5, self.subFont, (240, 240, 240))
        self.six = Button('6', (s * 6, self.h * 0.8, s, self.h * 0.2), 6, self.subFont, (240, 240, 240))
        self.seven = Button('7', (s * 7, self.h * 0.8, s, self.h * 0.2), 7, self.subFont, (240, 240, 240))
        self.eight = Button('8', (s * 8, self.h * 0.8, s, self.h * 0.2), 8, self.subFont, (240, 240, 240))

        self.buttons = [self.none, self.flag, self.mine, self.mineAct, self.wrongFlag, self.zero, self.one,
                        self.two, self.three, self.four, self.five, self.six, self.seven, self.eight]

    def draw(self):
        self.win.fill((240, 240, 240))

        self.title.draw(self.win)

        for button in self.buttons:
            button.draw(self.win, self.focus==button)

        self.win.blit(self.img, self.imgRect)

        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.focus:
                        if not self.testing:
                            types = loadTypes()
                            types[self.focus.func] = self.avg
                            dumpTypes(types)

                            dumpImage(self.focus.func, self.arr)
                    self.running[0] = False
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    self.focus = None
                    for button in self.buttons:
                        if pygame.Rect(*button.rect).collidepoint(x, y):
                            if button == self.focus:
                                self.focus = None
                            else:
                                self.focus = button

            self.draw()
            self.clock.tick(24)
