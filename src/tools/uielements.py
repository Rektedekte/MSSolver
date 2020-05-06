import pygame


def drawtxt(txt, font, color, cord, anchor, win):
    textSurface = txtSurf(txt, font, color)
    textSurf, textRect = textSurface, textSurface.get_rect()
    if anchor == "c":
        textRect.center = cord
    elif anchor == "r":
        textRect.midright = cord
    elif anchor == "l":
        textRect.midleft = cord
    win.blit(textSurface, textRect)


def txtSurf(txt, font, color):
    return font.render(txt, True, color)


class Button:
    def __init__(self, txt, rect, func, font, color):
        self.txt = str(txt)
        self.font = font
        self.rect = rect
        self.func = func
        self.color = color

    def draw(self, win, focus=False):
        pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.rect(win, [0]*3 if not focus else (255, 0, 0), self.rect, 2)
        if self.txt:
            drawtxt(self.txt, self.font, [0] * 3, (self.rect[0] + self.rect[2] // 2, self.rect[1] + self.rect[3] // 2), 'c', win)


class InputBox(Button):
    def __init__(self, var, t, rect, font, color, low=None, high=None):
        Button.__init__(self, var[0], rect, None, font, color)
        self.var = var
        self.t = t
        if self.t == int:
            if type(low) == int:
                self.low = low
            else:
                self.low = -float('inf')

            if type(high) == int:
                self.high = high
            else:
                self.high = float('inf')

    def apply(self):
        if self.t == int:
            if self.txt == '': self.txt = '0'
        self.var[0] = self.t(self.txt)

    def valid(self, txt):
        try:
            if self.t == int:
                if txt == '': txt = '0'

            temp = self.t(txt)
            if self.t == int:
                return self.low <= temp <= self.high

            return True
        except:
            return False

    def backspace(self):
        if len(self.txt) != 0:
            txt = self.txt[:-1]
            if self.valid(txt):
                self.txt = txt
                self.apply()

    def addChar(self, char):
        if len(self.txt) >= 17:
            return
        txt = self.txt + char
        try:
            if txt[0] == '0':
                txt = txt[1:]
        except IndexError:
            pass
        if self.valid(txt):
            self.txt = txt
            self.apply()

    def inputBoxDraw(self, win, focus):
        pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.rect(win, [200, 0, 0] if focus else [0]*3, self.rect, 2)
        drawtxt('"{}"'.format(self.txt) if self.t == str else self.txt, self.font, [0] * 3, (self.rect[0] + self.rect[2] // 2, self.rect[1] + self.rect[3] // 2), 'c', win)


class TextField:
    def __init__(self, txt, cord, font, anchor):
        self.txt = txt
        self.cord = cord
        self.font = font
        self.anchor = anchor

    def draw(self, win):
        drawtxt(self.txt, self.font, [0] * 3, self.cord, self.anchor, win)


class RadioButtons:
    def __init__(self, buttons, focus):
        self.buttons = buttons
        self.focus = [button for button in self.buttons if button.func == focus[0]][0]
        self.var = focus

    @property
    def val(self):
        return self.focus.func

    def onClick(self, button):
        self.focus = button
        self.var[0] = button.func

    def draw(self, win):
        for button in self.buttons:
            button.draw(win)

        drawtxt('X', self.focus.font, [0] * 3, (self.focus.rect[0] + self.focus.rect[2] // 2, self.focus.rect[1] + self.focus.rect[3] // 2), 'c', win)
