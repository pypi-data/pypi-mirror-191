import os
from pyPman.utilities import utils
from pyPman.install import utils as install_utils


class SetupCommandGenerator(install_utils.CommandInitializer):
    def __init__(self, *args):
        super(SetupCommandGenerator, self).__init__(*args)

    @property
    def importer(self):
        return [
            "import os",
            "import sys",
            "from glob import glob",
            "from shutil import rmtree",
            "from setuptools import setup",
            "",
            "try:",
            "   from setuptools.command.clean import clean as clean_command",
            "except ImportError as err:",
            "   from distutils.command.clean import clean as clean_command",
        ]

    @property
    def cleanClass(self):
        return [
            "class Clean(clean_command):",
            "   def run(self):",
            "       clean_command.run(self)",
            "       delete_in_root = ['build', 'dist', '*.egg-info', '.tox', '.eggs', '.cache']",
            "       delete_everywhere = ['__pycache__', '*.pyc']",
            "",
            "       for candidate in delete_in_root:",
            "           rmtree_glob(candidate)",
            "",
            "       for visible_dir in glob('[A-Za-z0-9]*'):",
            "           for candidate in delete_everywhere:",
            "               rmtree_glob(os.path.join(visible_dir, candidate))",
            "               rmtree_glob(os.path.join(visible_dir, '*', candidate))",
        ]

    @property
    def globRmtreeDef(self):
        return [
            "def rmtree_glob(candidate):",
            "   for fobj in glob(candidate):",
            "       try:",
            "           rmtree(fobj)",
            "           print('%s/ removed from project' % fobj)",
            "       except OSError:",
            "           try:",
            "               os.remove(fobj)",
            "               print('%s/ removed from project' % fobj)",
            "           except OSError:",
            "               print('Unable to clean the %s/ from project' % fobj)",
        ]

    @property
    def readFileDef(self):
        return [
            "def read_file(path=None, file_name=None):",
            "   path = path or '.'",
            "   file_path = os.path.join(path, file_name)",
            "   print('Reading file %s' % file_path)",
            "   with open(file_path) as fd:",
            "       return fd.read()",
        ]

    @property
    def mainExecution(self):
        return [
            # TODO: Change package name once everything is completed
            "packageName = '%s'" % self.package_dict['package'],
            "exec(read_file(path=os.path.join('.', packageName), file_name='__init__.py'))",
            "version = __version__",
            "projectName = __name__",
            "readmeData = read_file(file_name='README.md')",
            "licenseData = read_file(file_name='LICENSE')",
        ]

    @property
    def basicSetup(self):
        dependencyStr = ", ".join([
            "'%s'" % "==".join(module) if module[1] else "'%s'" % module[0] for module in self.package_dict['dependency']
        ])
        packageStr = ', '.join(
            [
                # "%s.initialize" % packageName
                '"%s.{}" % packageName'.format(pkg) for pkg in self.package_dict['module']
            ]
        )
        return [
            "setup(",
            "   name=packageName,",
            # TODO: Change this
            "   description='%s'," % self.package_dict['description'],
            "   version=version,",
            "   packages=[",
            "       packageName,",
            "       # Add modules under your package to build while installing your module",
            "       # Like packageName.utilities, <your packageName>.<module under your package>",
            "       %s" % packageStr,
            "   ],",
            "   install_requires=[",
            # TODO: Add dependency modules
            "       %s" % dependencyStr,
            "       # Add your project requirements (External Modules) here",
            "   ],",
            # TODO: Assign license here
            "   license='%s'," % self.package_dict['license'],
            "   long_description_content_type='text/markdown',",
            "   long_description=readmeData,",
            "   author=', '.join(__author__),",
            "   author_email=', '.join(__author_email__),",
            # TODO: Assign url if exists
            "   url='%s'," % self.package_dict['url'] if self.package_dict['url'] else "",
            "   classifiers=[",
            "   # See https://pypi.org/pypi?%3Aaction=list_classifiers",
            "       '',",
            "   ],",
            "   python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',",
            "   data_files=[",
            "       'README.md',",
            "       'LICENSE',",
            "   ],",
            "   entry_points={",
            # TODO: Fill entry point if needed
            "       'console_scripts': [",
            "           # Change the <cli_cmd> to your preferred name",
            "           'cli_cmd=%s.%s:cli'," % (
                            self.package_dict['package'],
                            os.path.splitext(self.package_dict['main'])[0]
                        ),
            "       ],",
            "       'gui_scripts': [",
            "           # Change the <cli_cmd_ui> to your preferred name or",
            "           # remove this 'gui_scripts' keyValue pair if gui app is not required for you module",
            "           'cli_cmd_ui=%s.%s:cli_ui'," % (
                            self.package_dict['package'],
                            os.path.splitext(self.package_dict['main'])[0]
                        ),
            "       ],",
            "   },",
            "   cmdclass={",
            "       'clean': Clean",
            "   },",
            ")",
        ]


def commands(package_dict):
    cmd_gen = SetupCommandGenerator(package_dict)
    setup_file = utils.build_cmd_file(cmd_gen.initializer, script_list=[], class_or_def=False)
    setup_file = utils.build_cmd_file(cmd_gen.importer, script_list=setup_file, class_or_def=False)
    setup_file = utils.build_cmd_file(cmd_gen.cleanClass, script_list=setup_file)
    setup_file = utils.build_cmd_file(cmd_gen.globRmtreeDef, script_list=setup_file)
    setup_file = utils.build_cmd_file(cmd_gen.readFileDef, script_list=setup_file)
    setup_file = utils.build_cmd_file(cmd_gen.mainExecution, script_list=setup_file)
    setup_file = utils.build_cmd_file(cmd_gen.basicSetup, script_list=setup_file)
    setup_file.append('')
    return "\n".join(setup_file)
