import os
import click
import logging

from pyPman.initialize import projectInitialize as pInit

log = logging.getLogger(__name__)


class ModuleSelector(click.Option):
    def __init__(self, *args, **kwargs):
        nargs = kwargs.pop('nargs', -1)
        assert nargs == -1, 'nargs, if set, must be -1 not {}'.format(nargs)
        super(ModuleSelector, self).__init__(*args, **kwargs)
        self._module_parser = None

    def add_to_parser(self, parser, ctx):
        def parser_process(value, state):
            done = False
            value = [value]
            value += state.rargs
            state.rargs[:] = []
            value = tuple(value)


def check_for_dependency(dependency, package_dict):
    module = dependency[0]
    for savedModule in package_dict['dependency']:
        if module == savedModule[0]:
            return True
    return False


def check_for_dep_version(dependency, package_dict):
    module = dependency[0]
    m_version = None
    if len(dependency) == 2:
        m_version = dependency[1]
    if not m_version:
        return True
    for savedModule in package_dict['dependency']:
        if module == savedModule[0]:
            if m_version == savedModule[1]:
                return True
    return False


def check_for_module(module, package_dict):
    for added_module in package_dict['module']:
        if added_module == module:
            return True
    return False


def create_directory(output, dir_name):
    dir_path = os.path.join(output, dir_name)
    if os.path.exists(dir_path):
        log.warning("Directory name already exists.")
        return

    os.makedirs(dir_path)
    log.info("%s directory created in %s" % (dir_name, output))


def create_file(output, file_name="__init__.py"):
    if not os.path.exists(output):
        log.warning("Directory doesn't exists, Creating the directory")
        dir_path = os.path.dirname(output)
        dir_name = os.path.basename(output)
        create_directory(dir_path, dir_name)

    file_path = os.path.join(output, file_name)

    if os.path.exists(file_path):
        log.warning("Filename %s already exists in %s" % (file_name, output))
        return

    with open(file_path, 'w') as fd:
        fd.write("# %s created with PyProjectManager, you can remove this line later" % file_name)
    log.info("%s file created in %s" % (file_name, output))


def write_file(file_path, data=None):
    if not os.path.exists(file_path):
        dir_path = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        create_file(dir_path, file_name=file_name)
    with open(file_path, 'w') as fd:
        fd.write(data)
    log.info("Data written into file %s" % file_path)


def build_cmd_file(list_of_commands, script_list=[], class_or_def=True):
    if class_or_def:
        script_list.extend(["", ""])
    else:
        script_list.append("")
    script_list.extend(list_of_commands)
    return script_list
