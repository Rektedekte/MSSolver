from multiprocessing import Process, Array
import pygame

clock = pygame.time.Clock()


def OpenProcess(target, args, source=None, bg=None):
    if source:
        source.minimize()
        RunProcess(target, args, bg)
        source.restore()

    else:
        RunProcess(target, args, bg)


def RunProcess(target, args, bg=None):
    running = Array('b', [True])
    try:
        om = Process(target=target, args=tuple(args) + (running,))
        om.start()
        while running[0]:
            if bg:
                bg()
            clock.tick(24)
        om.join()
    except:
        pass


def MinimizeAndExecute(target, args, source):
    source.minimize()
    target(*args)
    source.restore()
