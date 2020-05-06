from tools.openprocess import OpenProcess
from tools.uielements import Button
from tools.window import Window
from settings import SettingsMenu
from ai import AI
import pygame
import sys


class MainScreen(Window):
    def __init__(self):
        super().__init__(500, 300, 'Menu')

        main_font = pygame.font.Font('fonts/OpenSans-SemiBold.ttf', 80)
        sub_font = pygame.font.Font('fonts/OpenSans-Regular.ttf', 50)
        bg_color = (230, 230, 230)

        self.startButton = Button('Solve', (self.w * 0.03, self.h * 0.05, self.w * 0.94, self.h * 0.47), self.solve, main_font, bg_color)
        self.settingsButton = Button('Settings', (self.w * 0.03, self.h * 0.55, self.w * 0.46, self.h * 0.41), self.openSettings, sub_font, bg_color)
        self.exitButton = Button('Exit', (self.w * 0.51, self.h * 0.55, self.w * 0.46, self.h * 0.41), self.exit, sub_font, bg_color)
        self.buttons = self.startButton, self.settingsButton, self.exitButton

        self.bg_color = bg_color

        self.run()

    def solve(self):
        OpenProcess(AI, [], source=self, bg=self.backgroundTick)

    def openSettings(self):
        OpenProcess(SettingsMenu, [], source=self, bg=self.backgroundTick)

    def exit(self):
        sys.exit()

    def draw(self):
        self.win.fill(self.bg_color)

        for button in self.buttons:
            button.draw(self.win)

        pygame.display.update()

    def run(self):
        self.draw()
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()

                        for button in self.buttons:
                            if pygame.Rect(*button.rect).collidepoint(x, y):
                                button.func()

            self.clock.tick(24)
