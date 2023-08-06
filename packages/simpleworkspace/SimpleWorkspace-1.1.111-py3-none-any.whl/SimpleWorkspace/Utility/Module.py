import sys as _sys
import importlib as _importlib
from importlib import util as _util
import pkg_resources as _pkg_resources
import subprocess as _subprocess

def RequireModules(modules: list[str]) -> bool:
    '''
    Checks if python modules are installed, otherwise tries to install them
    '''
    
    required = modules
    installed = {pkg.key for pkg in _pkg_resources.working_set}
    missing = required - installed
    if missing:
        print("Please wait a moment, application is missing some modules. These will be installed automatically...")
        python = _sys.executable
        for i in missing:
            try:
                _subprocess.check_call([python, "-m", "pip", "install", i])
            except Exception as e:
                pass
    _importlib.reload(_pkg_resources)
    installed = {pkg.key for pkg in _pkg_resources.working_set}
    missing = required - installed
    if missing:
        print("Not all required modules could automatically be installed!")
        print("Please install the modules below manually:")
        for i in missing:
            print("    -" + i)
        return False
    return True

def ImportModuleDynamically(moduleName, path):
    '''
    @param moduleName: freely name the module to import
    @param path: full path to the python module
    '''
    spec = _util.spec_from_file_location(moduleName, path)
    mod = _util.module_from_spec(spec)
    _sys.modules[moduleName] = mod
    spec.loader.exec_module(mod)
    return mod