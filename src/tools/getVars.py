import json
import numpy


def loadSettings():
    with open('./settings/config.txt', 'r') as f:
        return json.load(f)


def dumpSettings(obj):
    with open('./settings/config.txt', 'w') as f:
        json.dump(obj, f)


def loadOffset():
    return loadSettings()["offset"]


def dumpOffset(obj):
    config = loadSettings()
    config["offset"] = obj
    dumpSettings(config)


def loadTypes():
    with open('./settings/types.txt', 'r') as f:
        d = json.load(f)

    nd = {}
    for key, val in d.items():
        if key == 'null':
            nd[None] = val
        elif key in ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
            nd[int(key)] = val
        else:
            nd[key] = val

    return nd


def dumpTypes(obj):
    with open('./settings/types.txt', 'w') as f:
        json.dump(obj, f)


def loadImage(img):
    try:
        with open('./images/{}.txt'.format(img), 'r') as f:
            return numpy.array(json.load(f), dtype=int)
    except Exception:
        return False


def dumpImage(name, img):
    with open('./images/{}.txt'.format(name), 'w+') as f:
        json.dump(img.tolist(), f)
