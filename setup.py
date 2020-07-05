from cx_Freeze import setup, Executable

base = None    

executables = [Executable("operaciones.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "operaciones",
    options = options,
    version = "1.0",
    description = 'operaciones',
    executables = executables
)