import pygame
from tools.window import Window
from tools.uielements import txtSurf, drawtxt


class ErrorScreen(Window):
    def __init__(self, descrep, running=None):
        if running is None:
            running = [True]
        self.running = running

        super().__init__(1000, 300, 'Error')

        self.descrep = descrep

        self.titleFont = pygame.font.Font('fonts/OpenSans-SemiBold.ttf', 50)
        self.subFont = pygame.font.Font('fonts/OpenSans-Regular.ttf', 30)

        self.title = txtSurf('Error', self.titleFont, [0]*3)

        self.divider = ((self.w * 0.05, self.h * 0.2), (self.w * 0.95, self.h * 0.2))

        self.topText = txtSurf('An error occurred doing execution of the program.', self.subFont, [0]*3)
        self.subText = txtSurf('The following problems were found:', self.subFont, [0]*3)

        self.descreps = []
        for des in descrep:
            self.descreps.append(txtSurf(des, self.subFont, [0]*3))

        self.run()

    def draw(self):
        self.win.fill((240, 240, 240))

        drawtxt('Error', self.titleFont, (0, 0, 0), (self.w * 0.5, self.h * 0.075), 'c', self.win)

        pygame.draw.line(self.win, (50, 50, 50), *self.divider)

        drawtxt('An error occurred doing execution of the program', self.subFont, (0, 0, 0), (self.w * 0.5, self.h * 0.3), 'c', self.win)
        drawtxt('The following problems were found:', self.subFont, (0, 0, 0), (self.w * 0.5, self.h * 0.4), 'c', self.win)

        o = self.h * 0.6

        for i, des in enumerate(self.descrep):
            drawtxt(des, self.subFont, (0, 0, 0), (self.w * 0.5, o + self.h * 0.1 * i), 'c', self.win)

        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running[0] = False
                    return

            self.draw()
            self.clock.tick(24)
