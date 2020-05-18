import win32com.client
import win32con
import win32gui
import pygame
import sys


class Window:
    def __init__(self, w, h, name=None, icon=None, pygameFlags=None):
        self.w = w
        self.h = h

        pygame.init()

        if pygameFlags:
            self.win = pygame.display.set_mode((self.w, self.h), flags=pygameFlags)
        else:
            self.win = pygame.display.set_mode((self.w, self.h))

        self.w, self.h = self.win.get_size()

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

        self.hwnd = win32gui.FindWindow(None, self.winTitle)

    def getHandle(self):
        self.hwnd = win32gui.FindWindow(None, self.winTitle)

    def minimize(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_MINIMIZE)

    def restore(self):
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(self.hwnd)

    def move(self, l, t):
        win32gui.MoveWindow(self.hwnd, l - 7, t,  l + self.win.get_width() + 14, t + self.win.get_height() + 45, True)

    def backgroundTick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        try:
            self.draw()
        except AttributeError:
            pass
