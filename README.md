# MSSolver

This is a Minesweeper solver built in python. The ui is made with pygame, and multiple windows is managed with multiprocessing. This can create overhead on slower computers. The solver uses the pywin32 and win32gui packages, and only works on windows based machines. The solver is built to be as versatile as possible, and includes support for custom images, gameboxes and mouse and keyboard inputs.


## What you need:
* Python 3.5 / 3.6
* Windows (or any system that supports pywin32 and win32gui)


## Dependencies:
* numpy
* pygame
* pywin32
* win32gui
* pynput

## How to use:
* Create python 3.5 or 3.6 environment
* Activate the environment
* Cd into the MSSolver folder and "pip install -r requirements.txt"
* Cd into src folder
* "python run.py"

## Setting up the solver settings:
In order to use the solver, you will need to set it up. Here are all the settings and what they do:
* Width: The width of the minesweeper grid
* Height: The height of the minesweeper grid
* Mine Count: The amount of mines in the game (total)
* BF_LIMIT: Amount of cells in a border before the solver results to simplifying it. Raising the limit can cause performence problems
* FPS: The expected fps of the minesweeper game. Raising the limit will make the solver run faster, but it can be less stable
* Reveal Field: The button used to reveal a cell. Can be changed like in video games
* Place Flag: The button used to place a flag. Can be changed like in video games
* Reveal Neigh: The button used to reveal the neighbors of a cell. Can be changed like in video games
* Image Mode: The mode that the solver uses to find the game. fullscreen targets the entire screen, window targets a window
* Win Name: The name of the target window. Ties in with image mode
* GameBox Manager: Tool that allows you to select the area where the game takes place. Only mark the grid, not the entire window
* Image Manager: Tool that allows you to manage the images that the solver uses to determine what a specific cell is

All of the options need to be adjusted to your game. If you don't know what to place in BF_LIMIT, leave it be. Raising the value can mean more accurate solving, but will slow the game down significantly (exponentially). The FPS option doesn't need to be changed, but if you are running a minesweeper version with a higher than 24 fps, it can speed the program up a lot.

If something goes wrong, you can always use the reset_settings.py script to reset them to default (this uses the local default settings)

### Known issues:
* The solver does not support animated versions of minesweeper. This includes the new official Microsoft minesweeper.
* The settings menu sometimes freezes after typing in a parameter. Solved by closing and opening the window.
* There is significant overhead on slower computers when opening a new window, caused by the use of multiprocessing.
