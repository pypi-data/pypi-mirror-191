import sys
import subprocess
from importlib_metadata import version, PackageNotFoundError

def get_module_version(module, module_version=None, tries=0):
    if module_version:
        return module_version
    try:
        return version(module)
    except PackageNotFoundError:
        print("%s Trying to install '%s'..." % (tries + 1, module))
        if module_version:
            subprocess.call([sys.executable, '-m', 'pip', 'install', '{0}=={1}'.format(module, module_version)])
        else:
            subprocess.call([sys.executable, '-m', 'pip', 'install', '{0}'.format(module)])
        if tries == 2:
            print("Unable to find the package '%s' from PyPi, Please ensure before adding" % module)
            return
        tries += 1
        return get_module_version(module, module_version, tries=tries)
    except:
        print("Unable to find the issue, please contact sunil.nerella39@gmail.com for solution")

