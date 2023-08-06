# PyProjectManager
Python project manager smooths workflow to create, install and maintain python projects

Requirements
------------
The package is tested and working with Click 7.1.1. Other required packages are specified in setup files.

Method of installation
----------------------

To install Python Project manager from PyPi run this command in terminal

```
pip install pyPman
```

Or

To clone it from github : 

```
git clone https://github.com/sunilk-n/PyProjectManager.git
```
Then use python directly in the main folder
```
python setup.py sdist
```
To get the ".gz" file

Complete help information about `init`:
---------------------------------------

* pyPman init : Starts project initialization
* `pyPman init [-p <projectName>]` : Starts project initialization setting projectName as provided
* `pyPman init [-p <projectName> -d <dependancy>]` : Adds 3rd party dependancy modules to the project
        Usage: `pyPman init -p <projectName> -d <moduleName>[==<module_version>]`....
                Mentioning no version will take the latest version of specified dependency
            * Ex: `pyPman init -p PyProjectManager -d click` (or)
            * Ex: `pyPman init -p PyProjectManager -d click==7.1.1`
            * Ex: `pyPman init -p PyProjectManager -d click==7.1.1 -d traVer`...(For multiple dependencies
* `pyPman init [-p <projectName> -m <module> -m <module>...]` : Adds user defined module package to the project
    - Usage: `pyPman init -p <projectName> -m <moduleName>`
        * Ex: `pyPman init -p PyProjectManager -m testModule -m testModule2`


Complete help information about `install`:
------------------------------------------
* `pyPman install [-p <projectName>]` : Starts installing project to the current directory
    - Usage: `pyPman install -p <projectName>`
        * Ex: `pyPman install -p PyProjectManager`
