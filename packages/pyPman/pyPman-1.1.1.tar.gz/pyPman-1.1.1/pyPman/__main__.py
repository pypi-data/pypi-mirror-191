"""
    Main entry point for the application to start
"""
import sys
import os as _os
import click
import logging

from pyPman import __version__
from pyPman.initialize import projectInitialize as pInit
from pyPman.install import builder as p_build
from pyPman.utilities import utils
from pyPman.utilities import moduleVersion

OUTPUT_DIR = _os.getcwd()
log = logging.getLogger(__name__)


class ListParamType(click.ParamType):
    name = 'list'

    def convert(self, value, param, ctx):
        return value.split('==')


@click.group()
@click.version_option(version=__version__, prog_name="PyProjectManager")
@click.help_option("-h", "--help", help="Displays this help options and exits")
@click.option('--verbose', is_flag=True, help='Displays all the log.')
@click.pass_context
def cli(context, verbose):
    if verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)


@cli.command()
@click.pass_context
@click.help_option("-h", "--help", help="Displays this help options and exits")
@click.option("--project", "-p", type=str, default=None, help="Project name")
@click.option("--dependency", "-d", type=ListParamType(), multiple=True,
              help="Add dependency projects to the existing project with module name and version(module_name==version")
@click.option("--module", '-m', type=str, multiple=True, help="Add new module to the project")
def init(context, project, dependency, module):
    logger = """
This utility will walk you through creating a setup.py file. It only covers the most common items, and tries to guess sensible defaults.

See `pyPman help install` for definitive documentation on these fields and exactly what they do.

Use `pyPman install -p <projectName>` afterwards to install a package and save it as a dependency in the setup.py file.

Press ^C at any time to quit.
    """
    if dependency:
        if not project:
            log.warning("Please specify the project name to add dependency by adding --project to command")
            return

        package_dict = {}
        if pInit.check_for_project(OUTPUT_DIR, pkg_file=project):
            package_dict = pInit.get_project_details(OUTPUT_DIR, pkg_file=project)
        if not package_dict:
            log.warning("Unable to find the project {0}, Please run `pyPman init --project {0}` to add dependency".format(
                project
            )
            )
            return
        is_updated = False
        for depend in dependency:
            log.info("Adding dependency for {0}".format(depend[0]))
            if len(depend) > 2:
                log.error("Arguments for dependency must be either <Dependency>==<version> or only <Dependency>")
                sys.exit()
            dep = False
            if utils.check_for_dependency(depend, package_dict):
                dep = True
                if utils.check_for_dep_version(depend, package_dict):
                    log.warning("Dependency '%s' already added to the project" % depend[0])
                    continue
            if len(depend) == 2:
                if dep:
                    for i, module in enumerate(package_dict['dependency']):
                        if module[0] == depend[0]:
                            package_dict['dependency'].pop(i)
                            is_updated = True
                            break

                m_version = moduleVersion.get_module_version(depend[0], module_version=depend[1])
                if not m_version:
                    # click.echo("Unable to find the module/module version. Exiting...")
                    log.warning("Unable to find the {0} or {1} version.".format(depend[0], depend[1]))
                    continue
                    # sys.exit()
                else:
                    package_dict['dependency'].append(depend)
                    is_updated = True
            elif len(depend) == 1:
                m_version = moduleVersion.get_module_version(depend[0])
                package_dict['dependency'].append([depend[0], m_version])
                is_updated = True
            click.echo("Dependency updated with %s module" % depend[0])
        if is_updated:
            pInit.create_files(OUTPUT_DIR, ".%s.json" % project, data=package_dict)
        if not module:
            return

    if module:
        if not project:
            log.warning("Please specify the project name to add dependency by adding --project to command")
            return
        package_dict = {}
        if pInit.check_for_project(OUTPUT_DIR, pkg_file=project):
            package_dict = pInit.get_project_details(OUTPUT_DIR, pkg_file=project)
        if not package_dict:
            log.warning("Unable to find the project {0}, Please run `pyPman init --project {0}` to add dependency"
                .format(project)
            )
            return
        for mod in module:
            if utils.check_for_module(mod, package_dict):
                log.warning("Module '%s' already exists in the project" % mod)
                continue
            package_dict['module'].append(mod)
            pInit.create_files(OUTPUT_DIR, ".%s.json" % project, data=package_dict)
            click.echo("Module '%s' added to project" % mod)
        return

    click.echo(message=logger)
    pInit.init_project(OUTPUT_DIR, project=project)


@cli.command()
@click.pass_context
@click.help_option("-h", "--help", help="Displays this help options and exits")
@click.option("--project", "-p", type=str, default=None, help="Project name")
# @click.option("project", type=str, help="Project name", required=True)
def install(context, project):
    click.echo(message="Starting installing from the saved data")
    package_dict = {}
    if pInit.check_for_project(OUTPUT_DIR, pkg_file=project):
        package_dict = pInit.get_project_details(OUTPUT_DIR, pkg_file=project)
    if not package_dict:
        log.warning("Unable to find the project {0}, Please run `pyPman init --project {0}` to add dependency".format(
                project
            )
        )
        return
    p_build.install(OUTPUT_DIR, package_dict)
    click.echo(message="%s project installed in %s directory" %(project, OUTPUT_DIR))


@cli.command()
@click.pass_context
@click.argument("option")
@click.help_option("-h", "--help", help="Displays this help options and exits")
def help(context, option):
    options = ['init', 'install']
    if not option in options:
        log.error("No option called '%s' in pyPman" % option)
        sys.exit()
    click.echo("Displays help for the option given %s" % option)

    helper_msg = ""
    if option == "init":
        helper_msg = """
Complete help information about init:
    * pyPman init : Starts project initialization
    * pyPman init [-p <projectName>] : Starts project initialization setting projectName as provided
    * pyPman init [-p <projectName> -d <dependancy>] : Adds 3rd party dependancy modules to the project
        Usage: pyPman init -p <projectName> -d <moduleName>[==<module_version>]....
                Mentioning no version will take the latest version of specified dependency
            * Ex: pyPman init -p PyProjectManager -d click (or)
            * Ex: pyPman init -p PyProjectManager -d click==7.1.1
            * Ex: pyPman init -p PyProjectManager -d click==7.1.1 -d traVer...(For multiple dependencies
    * pyPman init [-p <projectName> -m <module>] : Adds user defined module package to the project
        Usage: pyPman init -p <projectName> -m <moduleName>
            * Ex: pyPman init -p PyProjectManager -m testModule 
            * Ex: pyPman init -p PyProjectManager -m testModule1 -m testModule2 ...
        """

    elif option == "install":
        helper_msg = """
Complete help information about install:
    * pyPman install [-p <projectName>] : Starts installing project to the current directory
        Usage: pyPman install -p <projectName>
            * Ex: pyPman install -p PyProjectManager
        """

    click.echo(helper_msg)
