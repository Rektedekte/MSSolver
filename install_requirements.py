import subprocess
import sys
import contextlib
import platform


def install(package):
    '''
    installs a package using pip
    :param package: string
    '''
    subprocess.call([sys.executable, "-m", "pip", "install", package])


required = []
failed = []

inf = sys.version_info
if inf.major != 3 or (inf.minor != 5 and inf.minor != 6):
    print('ERROR: This library only supports python 3.5 or 3.6, not python {}.'.format('{}.{}'.format(inf.major, inf.minor)))
    sys.exit()

system = platform.system()
if system != 'Windows':
    print('ERROR: This library only supports Window, not {}.'.format(system))
    sys.exit()

# Try to open reqirements.txt file and read all required packages
try:
    with open("requirements.txt", "r") as file:
        file_lines = file.readlines()
    required = [line.strip().lower() for line in file_lines]
except FileNotFoundError:
    print("[ERROR] No requiremnts.txt file found")

if len(required) > 0:
    print("[INPUT] You are about to install {} packages, would you like to proceed (y/n):".format(len(required)), end=" ")
    ans = input()

    if ans.lower() == "y":
        for package in required:
            try:
                print("[LOG] Looking for", package)
                with contextlib.redirect_stdout(None):
                    __import__(package)
                print("[LOG]", package, "is already installed, skipping...")
            except ImportError:
                print("[LOG]", package, "not installed")

                try:
                    print("[LOG] Trying to install {} via pip".format(package))
                    print("[LOG] Installing", package)
                    install(package)
                    with contextlib.redirect_stdout(None):
                        __import__(package)
                    print("[LOG]", package, "has been installed")
                except Exception as e:
                    print("[ERROR] Could not install", package, "-", e)
                    failed.append(package)

    else:
        print("[STOP] Operation terminated by user")
else:
    print("[LOG] No packages to install")

if len(failed) > 0:
    print("[FAILED] {} package(s) were not installed. Failed package install(s):".format(len(failed)), end=" ")
    for x, package in enumerate(failed):
        if x != len(failed) - 1:
            print(package, end=",")
        else:
            print(package)