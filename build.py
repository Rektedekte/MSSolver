import cx_Freeze

executables = [cx_Freeze.Executable('reset_settings.py', base="Win32GUI")]

cx_Freeze.setup(

    name='Minesweeper Solver',

    options={"build_exe": {

    "packages": [
    'os', 'sys', 'json'
    ]}},
    
    executables=executables

)
