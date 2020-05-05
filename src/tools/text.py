def pydrawtxt(txt, font, color, cord, anchor, win):
    textSurface = font.render(txt, True, color)
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
