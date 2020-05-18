from tools.uielements import TextField, Button, RadioButtons, InputBox
from tools.uielements import drawtxt
from tools.window import Window
from tools.grab import gameBoxImg
from tools import getVars
import pygame


pw = 2


class OffsetManager(Window):
    def __init__(self, running=None):
        if running is None:
            running = [True]
        self.running = running

        vars = getVars.loadSettings()

        self.mode = vars["mode"]
        self.windowName = vars["window_name"]

        self.focusImg = gameBoxImg(o=False)

        if not self.focusImg:
            self.running[0] = False
            return

        self.nonFocusImg = self.focusImg.copy()
        self.nonFocusImg.set_alpha(200)

        super().__init__(*self.focusImg.get_size(), 'GameBox Manager', pygameFlags=None if self.mode=="Window" else pygame.FULLSCREEN)

        if self.mode == 'Window':
            self.restore()

        self.font = pygame.font.Font('fonts/OpenSans-Bold.ttf', 30)

        self.box = Box(self.w, self.h, getVars.loadOffset())

        self.focus = None
        self.inSensBox = False
        self.startSidePos = None
        self.startMousePos = None
        self.pw = pw

        self.createUI()

        self.run()

    def createUI(self):
        self.txtFields = []
        self.txtFields.append(TextField('Mode', (self.w - 150, 21.6), self.font, 'c'))
        self.txtFields.append(TextField('Snap:', (self.w - 300, 54), self.font, 'l'))
        self.txtFields.append(TextField('Drag:', (self.w - 300, 91.8), self.font, 'l'))

        snapButton = Button('', (self.w - 58, 41, 48, 37.8), 'Snap', self.font, None)
        dragButton = Button('', (self.w - 58, 75.6, 48, 37.8), 'Drag', self.font, None)
        self.mode = ['Snap']
        self.modeButtons = RadioButtons([snapButton, dragButton], self.mode)

        self.txtFields.append(TextField('Sens Div:', (self.w - 300, 135), self.font, 'l'))
        self.dragSen = [2]
        self.dragSenInputBox = InputBox(self.dragSen, int, (self.w - 96, 118.8, 84.6, 37.8), self.font, None, high=1000)

    def apply(self):
        getVars.dumpOffset(self.box.offset)

    def applyDrag(self, x, y):
        self.snapToSide(x, y)

        if self.focus == 'left':
            self.startMousePos = x
            self.startSidePos = self.box.left
        elif self.focus == 'right':
            self.startMousePos = x
            self.startSidePos = self.box.right
        elif self.focus == 'top':
            self.startMousePos = y
            self.startSidePos = self.box.top
        elif self.focus == 'bottom':
            self.startMousePos = y
            self.startSidePos = self.box.bottom

    def drag(self, x, y):
        if self.dragSen[0] == 0:
            return

        if self.focus == 'left':
            dif = x - self.startMousePos
            offset = dif // self.dragSen[0]
            targetPos = self.startSidePos + offset
            if targetPos >= self.box.right:
                self.box.left = self.box.right
            else:
                self.box.left = targetPos
        elif self.focus == 'right':
            dif = x - self.startMousePos
            offset = dif // self.dragSen[0]
            targetPos = self.startSidePos + offset
            if targetPos <= self.box.left:
                self.box.right = self.box.left
            else:
                self.box.right = targetPos
        elif self.focus == 'top':
            dif = y - self.startMousePos
            offset = dif // self.dragSen[0]
            targetPos = self.startSidePos + offset
            if targetPos >= self.box.bottom:
                self.box.top = self.box.bottom
            else:
                self.box.top = targetPos
        else:
            dif = y - self.startMousePos
            offset = dif // self.dragSen[0]
            targetPos = self.startSidePos + offset
            if targetPos <= self.box.top:
                self.box.bottom = self.box.top
            else:
                self.box.bottom = targetPos

    def unApplyDrag(self):
        self.focus = None

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
        self.win.fill((255, 255, 255))
        self.win.blit(self.nonFocusImg, (0, 0))

        focusCutOut = pygame.Surface(self.box.size)
        focusCutOut.blit(self.focusImg, (0, 0), self.box.rect)

        self.win.blit(focusCutOut, (self.box.offsetL, self.box.offsetT))

        pygame.draw.rect(self.win, (0, 255, 0), self.box.boxDrawRect, pw)

        drawtxt('Width: {}'.format(self.box.width), self.font, (0, 0, 0), (6, 22), 'l', self.win)
        drawtxt('Height: {}'.format(self.box.height), self.font, (0, 0, 0), (6, 54), 'l', self.win)

        for textField in self.txtFields:
            textField.draw(self.win)

        self.modeButtons.draw(self.win)
        self.dragSenInputBox.inputBoxDraw(self.win, self.inSensBox)

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
                    used = False

                    for button in self.modeButtons.buttons:
                        if pygame.Rect(*button.rect).collidepoint(x, y):
                            self.inSensBox = False
                            used = True
                            self.modeButtons.onClick(button)

                    if pygame.Rect(*self.dragSenInputBox.rect).collidepoint(x, y):
                        used = True
                        self.inSensBox = not self.inSensBox

                    if not used:
                        self.inSensBox = False
                        if self.mode[0] == "Snap":
                            self.snapToSide(x, y)
                        else:
                            self.applyDrag(x, y)

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.focus:
                        self.unSnapToSide()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.inSensBox = False

                    elif self.inSensBox:
                        if event.key == pygame.K_BACKSPACE:
                            self.dragSenInputBox.backspace()
                        else:
                            self.dragSenInputBox.addChar(event.unicode)

            if self.focus:
                if self.mode[0] == "Snap":
                    self.adjustSideToPos(*pygame.mouse.get_pos())
                else:
                    self.drag(*pygame.mouse.get_pos())

            self.draw()
            self.clock.tick(60)


class Box:
    def __init__(self, disWidth, disHeight, offset):
        self.disWidth = disWidth
        self.disHeight = disHeight

        self.left = offset["left"]
        self.right = disWidth - offset["right"]
        self.top = offset["top"]
        self.bottom = disHeight - offset["bottom"]

        if not self.isValid():
            self.left = 0
            self.right = disWidth
            self.top = 0
            self.bottom = disHeight

    @property
    def boxDrawRect(self):
        return self.left - pw, self.top - pw, self.width + 2 * pw - 1, self.height + 2 * pw - 1

    @property
    def rect(self):
        return self.left, self.top, self.width, self.height

    @property
    def offset(self):
        return {"left": self.offsetL, "right": self.offsetR, "top": self.offsetT, "bottom": self.offsetB}

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

    @property
    def size(self):
        return self.width, self.height

    def isValid(self):
        return self.right >= self.left and self.bottom >= self.top
