from . import getVars
from . import grab
import numpy as np


def CalibratePixelSize():
    img = grab.GameBox(o=True)

    if type(img) == bool:
        return False

    i = 5
    while i < 100:
        source = np.average(img[0:i, 0:i])
        target = np.average(img[i:i*2, i:i*2])

        if source == target:
            v = getVars.loadSettings()
            v["pixel_width"] = i
            getVars.dumpSettings(v)
            return True

        i += 1

    return False
