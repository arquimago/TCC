from cx_Freeze import setup, Executable
import sys

base = None

if sys.platform == 'win32':
    base = None


executables = [Executable("script.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "Automatizacao Experimentos",
    options = options,
    version = "0.3",
    description = 'bla bla bla',
    executables = executables
)