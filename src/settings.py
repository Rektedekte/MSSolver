from tools.uielements import TextField, InputBox, Button, RadioButtons
from tools.calibrate import CalibratePixelSize
from offsetmanager import OffsetManager
from imagemanager import ImageManager
from tools.openprocess import openProcess, minimizeAndExecute
from tools.window import Window
from tools import getVars
import pygame


class SettingsMenu(Window):
    def __init__(self, running=None):
        super().__init__(500, 550, 'Settings')

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
        self.titleField = TextField('Settings', (self.w // 2, self.h * 0.043), self.titleFont, 'c')

        left = self.w * 0.05

        self.txtField1 = TextField('Width:', (left, self.h * 0.15), self.txtFieldFont, 'l')
        self.txtField2 = TextField('Height:', (left, self.h * 0.21), self.txtFieldFont, 'l')
        self.txtField3 = TextField('Mine Count:', (left, self.h * 0.27), self.txtFieldFont, 'l')

        self.txtField4 = TextField('Pixel Size:', (left, self.h * 0.37), self.txtFieldFont, 'l')
        self.txtField5 = TextField('FPS:', (left, self.h * 0.43), self.txtFieldFont, 'l')

        self.txtField6 = TextField('Image Mode:', (self.w//2, self.h * 0.64), self.txtFieldFont, 'c')
        self.txtField7 = TextField('Window:', (left, self.h * 0.70), self.txtFieldFont, 'l')
        self.txtField8 = TextField('Full Screen:', (left, self.h * 0.76), self.txtFieldFont, 'l')

        self.txtField9 = TextField('Win Name:', (left, self.h * 0.86), self.txtFieldFont, 'l')

        self.txtFields = [self.titleField, self.txtField1, self.txtField2, self.txtField3, self.txtField4, self.txtField5, self.txtField6, self.txtField7, self.txtField8, self.txtField9]

    def createInputBoxes(self):
        n = 16.5
        n2 = 20
        offset = self.h * 0.13
        self.inputBox1 = InputBox(self.vars[0], int, (self.w*0.55, self.h//n*0 + offset, self.w*0.4, self.h//n2), self.inputBoxFontInt, self.bg_color, 0, 100)
        self.inputBox2 = InputBox(self.vars[1], int, (self.w*0.55, self.h//n*1 + offset, self.w*0.4, self.h//n2), self.inputBoxFontInt, self.bg_color, 0, 100)
        self.inputBox3 = InputBox(self.vars[2], int, (self.w*0.55, self.h//n*2 + offset, self.w*0.4, self.h//n2), self.inputBoxFontInt, self.bg_color, 0, 1000)
        offset += self.h * 0.04
        self.inputBox4 = InputBox(self.vars[3], int, (self.w*0.55, self.h//n*3 + offset, self.w*0.4, self.h//n2), self.inputBoxFontInt, self.bg_color, 0, 100)
        self.inputBox5 = InputBox(self.vars[4], int, (self.w*0.55, self.h//n*4 + offset, self.w*0.4, self.h//n2), self.inputBoxFontInt, self.bg_color, 0, 300)
        offset += self.h * 0.31
        self.inputBox6 = InputBox(self.vars[6], str, (self.w*0.55, self.h//n*6 + offset, self.w*0.4, self.h//n2), self.inputBoxFontStr, self.bg_color)

        self.inputBoxes = [self.inputBox1, self.inputBox2, self.inputBox3, self.inputBox4, self.inputBox5, self.inputBox6]

    def createRadioButtons(self):
        b1 = Button('', (self.w * 0.88, self.h * 0.66, self.w // 12.5, self.h // 16), 'Window', self.txtFieldFont, self.bg_color)
        b2 = Button('', (self.w * 0.88, self.h * 0.73, self.w // 12.5, self.h // 16), 'Fullscreen', self.txtFieldFont, self.bg_color)
        self.radioButton1 = RadioButtons([b1, b2], self.vars[5])

        self.radioButtons = [self.radioButton1]

    def createLines(self):
        self.lines = []
        self.lines.append(((self.w * 0.03, self.h * 0.10), (self.w * 0.97, self.h * 0.10)))
        self.lines.append(((self.w * 0.03, self.h * 0.32), (self.w * 0.97, self.h * 0.32)))
        self.lines.append(((self.w * 0.03, self.h * 0.59), (self.w * 0.97, self.h * 0.59)))
        self.lines.append(((self.w * 0.03, self.h * 0.81), (self.w * 0.97, self.h * 0.81)))

    def createButtons(self):
        self.button1 = Button('Calibrate Pixel Size', (self.w*0.05, self.h*0.472, self.w*0.9, self.h*0.09), self.callibratePixelSize, self.inputBoxFontStr, self.bg_color)
        self.button2 = Button('GameBox Manager', (self.w*0.05, self.h*0.902, self.w*0.44, self.h*0.08), self.openOffsetManager, self.inputBoxFontStr, self.bg_color)
        self.button3 = Button('Image Manager', (self.w * 0.51, self.h * 0.902, self.w * 0.44, self.h * 0.08), self.openImageManager, self.inputBoxFontStr, self.bg_color)
        self.buttons = [self.button1, self.button2, self.button3]

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

    def callibratePixelSize(self):
        self.dumpVars()
        minimizeAndExecute(CalibratePixelSize, [], self)
        self.loadVars()
        self.createInputBoxes()

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
                        if event.key == pygame.K_BACKSPACE:
                            self.focus.backspace()
                        else:
                            self.focus.addChar(event.unicode)

            self.draw()
            self.clock.tick(24)
