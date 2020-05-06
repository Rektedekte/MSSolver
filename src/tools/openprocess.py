from multiprocessing import Process, Array
import pygame

clock = pygame.time.Clock()


def openProcess(target, args, source=None, bg=None):
    if source:
        source.minimize()
        runProcess(target, args, bg)
        source.restore()

    else:
        runProcess(target, args, bg)


def runProcess(target, args, bg=None):
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


def minimizeAndExecute(target, args, source):
    source.minimize()
    target(*args)
    source.restore()
