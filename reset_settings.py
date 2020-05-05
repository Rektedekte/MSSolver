import json
import sys
import os

source = 'defaults/'
target = 'src/settings/'
all = ['offset.txt', 'types.txt', 'settings.txt']


def clearImages():
    for file in os.listdir('src/images'):
        os.remove('src/images/{}'.format(file))


def reset(args):
    vs = []
    for arg in args:
        with open(source + arg, 'r') as f:
            vs.append(json.load(f))

    for dump, arg in zip(vs, args):
        with open(target + arg, 'w+') as f:
            json.dump(dump, f)


def main():
    inputargs = sys.argv
    inputargs.pop(0)

    if len(inputargs) == 0:
        inputargs.append('all')

    if 'all' in inputargs:
        args = all
    else:
        args = list(dict.fromkeys((filter(lambda arg: arg in all, inputargs))))

    if len(args) == 0:
        raise ValueError('Missing arguments: 0 out of {} valid'.format(inputargs))

    if 'types.txt' in args:
        clearImages()

    reset(args)


if __name__ == '__main__':
    main()
