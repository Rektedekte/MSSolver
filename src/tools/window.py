from win32gui import FindWindow, ShowWindow, MoveWindow, SetForegroundWindow
from win32con import SW_MINIMIZE, SW_RESTORE
import pygame
import sys


class Window:
    def __init__(self, w, h, name=None, icon=None):
        self.w = w
        self.h = h

        pygame.init()
        self.win = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        if name:
            assert type(name) == str
            pygame.display.set_caption(name)
            self.winTitle = name

        else:
            self.winTitle = 'pygame display'

        if icon:
            assert type(icon) == str
            pygame.display.set_icon(pygame.image.load(icon).convert())

        self.hwnd = FindWindow(None, self.winTitle)

    def minimize(self):
        ShowWindow(self.hwnd, SW_MINIMIZE)

    def restore(self):
        ShowWindow(self.hwnd, SW_RESTORE)
        SetForegroundWindow(self.hwnd)

    def move(self, l, t):
        MoveWindow(self.hwnd, l - 7, t,  l + self.win.get_width() + 14, t + self.win.get_height() + 45, True)

    def backgroundTick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        try:
            self.draw()
        except AttributeError:
            pass
