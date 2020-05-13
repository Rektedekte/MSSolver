import json
import sys
import os

source = 'defaults/'
target = 'src/settings/'
all = ['types.txt', 'config.txt']


def clearImages():
    for file in os.listdir('src/images'):
        if file != ".gitignore":
            os.remove('src/images/{}'.format(file))


def reset(args):
    for arg in args:
        with open(source + arg, 'r') as s:
            with open(target + arg, 'w+') as t:
                json.dump(json.load(s), t)


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
