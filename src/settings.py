from tools.uielements import TextField, InputBox, Button, RadioButtons, KeyInputBox
from offsetmanager import OffsetManager
from imagemanager import ImageManager
from tools.openprocess import openProcess, minimizeAndExecute
from tools.window import Window
from tools import getVars
import pygame


class SettingsMenu(Window):
    def __init__(self, running=None):
        super().__init__(500, 600, 'Settings')

        if running is None:
            running = [True]
        self.running = running

        self.titleFont = pygame.font.Font('fonts/OpenSans-SemiBold.ttf', 40)
        self.txtFieldFont = pygame.font.Font('fonts/OpenSans-Regular.ttf', 30)
        self.inputBoxFontInt = pygame.font.Font('fonts/OpenSans-Regular.ttf', 25)
        self.inputBoxFontStr = pygame.font.Font('fonts/OpenSans-Regular.ttf', 20)
        self.bg_color = (240, 240, 240)

        self.loadVars()

        self.createTxtFields()
        self.createInputBoxes()
        self.createRadioButtons()
        self.createLines()
        self.createButtons()

        self.varNames = getVars.loadSettings().keys()

        self.focus = None
        self.run()

    def createTxtFields(self):
        left = self.w * 0.05

        self.txtFields = [
            TextField('Settings', (self.w // 2, self.h * 0.035), self.titleFont, 'c'),

            TextField('Width:', (left, self.h * 0.125), self.txtFieldFont, 'l'),
            TextField('Height:', (left, self.h * 0.185), self.txtFieldFont, 'l'),
            TextField('Mine Count:', (left, self.h * 0.245), self.txtFieldFont, 'l'),

            TextField('BF_LIMIT:', (left, self.h * 0.325), self.txtFieldFont, 'l'),
            TextField('FPS:', (left, self.h * 0.385), self.txtFieldFont, 'l'),

            TextField('Reveal Field:', (left, self.h * 0.465), self.txtFieldFont, 'l'),
            TextField('Place Flag:', (left, self.h * 0.525), self.txtFieldFont, 'l'),
            TextField('Reveal Neigh:', (left, self.h * 0.585), self.txtFieldFont, 'l'),

            TextField('Image Mode', (self.w//2, self.h * 0.665), self.txtFieldFont, 'c'),
            TextField('Window:', (left, self.h * 0.72), self.txtFieldFont, 'l'),
            TextField('Full Screen:', (left, self.h * 0.78), self.txtFieldFont, 'l'),

            TextField('Win Name:', (left, self.h * 0.86), self.txtFieldFont, 'l')
        ]

    def createInputBoxes(self):
        self.inputBoxes = []
        self.keyInputBoxes = []

        divider = 16.5
        height = self.h // 20
        offset = self.h * 0.1
        self.inputBoxes.append(InputBox(self.vars[0], int, (self.w*0.55, self.h//divider*0 + offset, self.w*0.4, height), self.inputBoxFontInt, self.bg_color, 0, 100))
        self.inputBoxes.append(InputBox(self.vars[1], int, (self.w*0.55, self.h//divider*1 + offset, self.w*0.4, height), self.inputBoxFontInt, self.bg_color, 0, 100))
        self.inputBoxes.append(InputBox(self.vars[2], int, (self.w*0.55, self.h//divider*2 + offset, self.w*0.4, height), self.inputBoxFontInt, self.bg_color, 0, 1000))
        offset += self.h * 0.02
        self.inputBoxes.append(InputBox(self.vars[3], int, (self.w*0.55, self.h//divider*3 + offset, self.w*0.4, height), self.inputBoxFontInt, self.bg_color, 0, 100))
        self.inputBoxes.append(InputBox(self.vars[4], int, (self.w*0.55, self.h//divider*4 + offset, self.w*0.4, height), self.inputBoxFontInt, self.bg_color, 0, 1000))
        offset += self.h * 0.02
        self.keyInputBoxes.append(KeyInputBox(self.vars[5], self.keyInputBoxUnhook, (self.w*0.55, self.h//divider*5 + offset, self.w*0.4, height), self.inputBoxFontInt, self.bg_color))
        self.keyInputBoxes.append(KeyInputBox(self.vars[6], self.keyInputBoxUnhook, (self.w*0.55, self.h//divider*6 + offset, self.w*0.4, height), self.inputBoxFontInt, self.bg_color))
        self.keyInputBoxes.append(KeyInputBox(self.vars[7], self.keyInputBoxUnhook, (self.w*0.55, self.h//divider*7 + offset, self.w*0.4, height), self.inputBoxFontInt, self.bg_color))
        offset += self.h * 0.22
        self.inputBoxes.append(InputBox(self.vars[9], str, (self.w*0.55, self.h//divider*8 + offset, self.w*0.4, height), self.inputBoxFontStr, self.bg_color))

    def createRadioButtons(self):
        b1 = Button('', (self.w * 0.88, self.h * 0.684, self.w // 12.5, self.h // 16), 'Window', self.txtFieldFont, self.bg_color)
        b2 = Button('', (self.w * 0.88, self.h * 0.75, self.w // 12.5, self.h // 16), 'Fullscreen', self.txtFieldFont, self.bg_color)

        self.radioButtons = [RadioButtons([b1, b2], self.vars[8])]

    def createLines(self):
        self.lines = [
            ((self.w * 0.03, self.h * 0.085), (self.w * 0.97, self.h * 0.085)),
            ((self.w * 0.03, self.h * 0.285), (self.w * 0.97, self.h * 0.285)),
            ((self.w * 0.03, self.h * 0.425), (self.w * 0.97, self.h * 0.425)),
            ((self.w * 0.03, self.h * 0.625), (self.w * 0.97, self.h * 0.625)),
            ((self.w * 0.03, self.h * 0.82), (self.w * 0.97, self.h * 0.82)),
        ]

    def createButtons(self):
        self.button1 = Button('GameBox Manager', (self.w*0.05, self.h*0.902, self.w*0.44, self.h*0.08), self.openOffsetManager, self.inputBoxFontStr, self.bg_color)
        self.button2 = Button('Image Manager', (self.w*0.51, self.h*0.902, self.w*0.44, self.h*0.08), self.openImageManager, self.inputBoxFontStr, self.bg_color)
        self.buttons = [self.button1, self.button2]

    @property
    def valid(self):
        if self.vars[0][0] == 0:
            return False
        if self.vars[1][0] == 0:
            return False
        if self.vars[3][0] == 0:
            return False
        if self.vars[4][0] == 0:
            return False
        return True

    def keyInputBoxUnhook(self):
        self.focus = None

    def openOffsetManager(self):
        self.dumpVars()
        openProcess(OffsetManager, [], self, self.backgroundTick)
        self.loadVars()
        self.createInputBoxes()
        self.createRadioButtons()

    def openImageManager(self):
        openProcess(ImageManager, [], self, self.backgroundTick)

    def loadVars(self):
        self.vars = [[var] for var in getVars.loadSettings().values()]

    def dumpVars(self):
        getVars.dumpSettings({k: v[0] for k, v in zip(self.varNames, self.vars)})

    def draw(self):
        self.win.fill(self.bg_color)

        for field in self.txtFields:
            field.draw(self.win)

        for box in self.inputBoxes:
            box.inputBoxDraw(self.win, box==self.focus)

        for keyBox in self.keyInputBoxes:
            keyBox.keyInputBoxDraw(self.win, keyBox==self.focus)

        for radioButton in self.radioButtons:
            radioButton.draw(self.win)

        for line in self.lines:
            pygame.draw.line(self.win, (50, 50, 50), *line)

        for button in self.buttons:
            button.draw(self.win)

        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.valid:
                        self.dumpVars()
                        self.running[0] = False
                        return

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.focus = None
                    x, y = pygame.mouse.get_pos()

                    for box in self.inputBoxes:
                        if pygame.Rect(*box.rect).collidepoint(x, y):
                            self.focus = box

                    for keyBox in self.keyInputBoxes:
                        if pygame.Rect(*keyBox.rect).collidepoint(x, y):
                            keyBox.onClick()
                            self.focus = keyBox

                    for radio in self.radioButtons:
                        for button in radio.buttons:
                            if pygame.Rect(*button.rect).collidepoint(x, y):
                                radio.onClick(button)

                    for button in self.buttons:
                        if pygame.Rect(*button.rect).collidepoint(x, y):
                            button.func()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.focus = None

                    elif self.focus:
                        if isinstance(self.focus, InputBox):
                            if event.key == pygame.K_BACKSPACE:
                                self.focus.backspace()
                            else:
                                self.focus.addChar(event.unicode)

            self.draw()
            self.clock.tick(24)
