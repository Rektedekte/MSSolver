from numpy import frombuffer
from . import getVars
import win32api
import win32gui
import win32con
import win32ui
import pygame


def minimize(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)


def restore(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)


def foregroundTitle():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())


def getHandle():
    settings = getVars.loadSettings()

    mode = settings[5]
    name = settings[6]

    if mode == 'Window':
        hwnd = win32gui.FindWindow(None, name)
    else:
        hwnd = win32gui.GetDesktopWindow()

    return hwnd


def GameBoxRect(hwnd=None):
    if hwnd is None:
        hwnd = getHandle()

    restore(hwnd)

    offset = getVars.loadOffset()

    try:
        rect = win32gui.GetWindowRect(hwnd)
    except:
        return False

    return rect[0] + offset[0], rect[2] - offset[1], rect[1] + offset[2], rect[3] - offset[3]


def GameBoxImg(hwnd=None, o=True):
    if hwnd is None:
        hwnd = getHandle()

    img = GameBox(hwnd, o)

    if type(img) == bool:
        return False

    img = img[::-1, :, :]
    pyimg = pygame.pixelcopy.make_surface(img)
    pyimg = pygame.transform.rotate(pyimg, 90)
    return pyimg


def GameBox(hwnd=None, o=True):
    if hwnd is None:
        hwnd = getHandle()

    if hwnd == 0:
        return False

    settings = getVars.loadSettings()

    mode = settings[5]

    try:
        if mode == 'Window':
            restore(hwnd)
            img = hwndToArr(hwnd)
        else:
            img = hwndToArr(hwnd)
    except:
        return False

    if o:
        offset = getVars.loadOffset()
        return img[offset[2]:-offset[3], offset[0]:-offset[1], 2::-1]
    return img[:, :, 2::-1]


def hwndToArr(hwnd):
    restore(hwnd)

    try:
        rect = win32gui.GetWindowRect(hwnd)
        w, h = rect[2] - rect[0], rect[3] - rect[1]
    except:
        w = win32api.GetSystemMetrics(0)
        h = win32api.GetSystemMetrics(1)

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()

    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)

    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)

    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    return img
