from tools.getVars import loadImage, dumpImage, loadTypes, dumpTypes
from tools.window import Window
from tools.uielements import Button
import pygame
import os


class ImageManager(Window):
    def __init__(self, running=None):
        if running is None:
            running = [True]
        self.running = running

        super().__init__(650, 700, 'Image Manager')
        self.restore()

        self.txtFont = pygame.font.Font('fonts/OpenSans-Light.ttf', 30)

        self.types = loadTypes()
        self.vars = list(self.types.keys())

        self.createTxtFields()
        self.createImgs()
        self.createButtons()

        self.run()

    def createTxtFields(self):
        s = self.h / len(self.vars)
        f = self.w / 3

        self.txtFields = []

        for i, name in enumerate(self.vars):
            self.txtFields.append(Button(str(name), (0, s * i, f, s), None, self.txtFont, (240, 240, 240)))

    def createImgs(self):
        self.imgs = []

        for name in self.vars:
            try:
                img = loadImage(name)[::-1, :, :]
                img = pygame.pixelcopy.make_surface(img)
                img = pygame.transform.rotate(img, 90)
                self.imgs.append(pygame.transform.scale(img, (40, 40)))
            except:
                self.imgs.append(None)

    def createButtons(self):
        s = self.h / len(self.vars)
        o = self.w / 3 * 2
        f = self.w / 3

        self.buttons = []

        for i, name in enumerate(self.vars):
            self.buttons.append(Button('Clear', (o, s * i, f, s), name, self.txtFont, (240, 240, 240)))

    def clear(self, name):
        self.types[name] = 0
        self.imgs[self.vars.index(name)] = None

    def apply(self):
        dumpTypes(self.types)

        for type, name in zip(self.imgs, self.vars):
            if type is None:
                if os.path.exists('images/{}.txt'.format(name)):
                    os.remove('images/{}.txt'.format(name))

    def draw(self):
        self.win.fill((240, 240, 240))

        for txtField in self.txtFields:
            txtField.draw(self.win)

        for i, img in enumerate(self.imgs):
            pygame.draw.rect(self.win, (0, 0, 0), (self.w / 3, self.h / 14 * i, self.w / 3, self.h / 14), 2)
            if type(img) == pygame.Surface:
                self.win.blit(img, (self.w / 2 - 25, i * 50 + 5))

        for button in self.buttons:
            button.draw(self.win)

        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.apply()
                    self.running[0] = False
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if pygame.Rect(*button.rect).collidepoint(x, y):
                            self.clear(button.func)

            self.draw()
            self.clock.tick(24)
