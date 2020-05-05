import cx_Freeze

executables = [cx_Freeze.Executable('run.py', base="Win32GUI")]

cx_Freeze.setup(

    name='Minesweeper Solver',

    options={"build_exe": {

    "packages": [
    'numpy', 'mouse', 'keyboard', 'random', 'sys', 'time', 'os',
    'json', 'win32api', 'win32gui', 'win32con', 'win32ui', 'multiprocessing'
    ],

    "include_files": [
    "settings", "images", "fonts", 'ai.py', 'errorscreen.py', 'imagemanager.py',
    'menu.py', 'offsetmanager.py', 'settings.py', 'typescreen.py', 'tools'
    ]}},

    executables=executables

)

"""import numpy
import mouse
import keyboard
import random
import sys
import time
import os
import json
import win32api
import win32gui
import win32con
import win32ui"""
