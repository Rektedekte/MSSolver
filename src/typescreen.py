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
        topButtonWidth = self.w / 5
        self.buttons.append(Button('Tile', (topButtonWidth * 0, self.h * 0.6, topButtonWidth, self.h * 0.2), 'tile', self.subFont, (240, 240, 240)))
        self.buttons.append(Button('Flag', (topButtonWidth * 1, self.h * 0.6, topButtonWidth, self.h * 0.2), 'flag', self.subFont, (240, 240, 240)))
        self.buttons.append(Button('Mine', (topButtonWidth * 2, self.h * 0.6, topButtonWidth, self.h * 0.2), 'mine', self.subFont, (240, 240, 240)))
        self.buttons.append(Button('MineA', (topButtonWidth * 3, self.h * 0.6, topButtonWidth, self.h * 0.2), 'activated_mine', self.subFont, (240, 240, 240)))
        self.buttons.append(Button('WrongF', (topButtonWidth * 4, self.h * 0.6, topButtonWidth, self.h * 0.2), 'incorrect_flag', self.subFont, (240, 240, 240)))
        bottomButtonWidth = self.w / 9
        self.buttons.append(Button('0', (bottomButtonWidth * 0, self.h * 0.8, bottomButtonWidth, self.h * 0.2), '0', self.subFont, (240, 240, 240)))
        self.buttons.append(Button('1', (bottomButtonWidth * 1, self.h * 0.8, bottomButtonWidth, self.h * 0.2), '1', self.subFont, (240, 240, 240)))
        self.buttons.append(Button('2', (bottomButtonWidth * 2, self.h * 0.8, bottomButtonWidth, self.h * 0.2), '2', self.subFont, (240, 240, 240)))
        self.buttons.append(Button('3', (bottomButtonWidth * 3, self.h * 0.8, bottomButtonWidth, self.h * 0.2), '3', self.subFont, (240, 240, 240)))
        self.buttons.append(Button('4', (bottomButtonWidth * 4, self.h * 0.8, bottomButtonWidth, self.h * 0.2), '4', self.subFont, (240, 240, 240)))
        self.buttons.append(Button('5', (bottomButtonWidth * 5, self.h * 0.8, bottomButtonWidth, self.h * 0.2), '5', self.subFont, (240, 240, 240)))
        self.buttons.append(Button('6', (bottomButtonWidth * 6, self.h * 0.8, bottomButtonWidth, self.h * 0.2), '6', self.subFont, (240, 240, 240)))
        self.buttons.append(Button('7', (bottomButtonWidth * 7, self.h * 0.8, bottomButtonWidth, self.h * 0.2), '7', self.subFont, (240, 240, 240)))
        self.buttons.append(Button('8', (bottomButtonWidth * 8, self.h * 0.8, bottomButtonWidth, self.h * 0.2), '8', self.subFont, (240, 240, 240)))

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
