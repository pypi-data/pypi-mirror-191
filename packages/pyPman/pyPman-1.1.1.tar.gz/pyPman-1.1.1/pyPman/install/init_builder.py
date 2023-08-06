import os

import pyPman
from pyPman.utilities import utils
from pyPman.install.utils import CommandInitializer


class InitCommandGenerator(CommandInitializer):
    def __init__(self, *args):
        super(InitCommandGenerator, self).__init__(*args)

    @property
    def assigner(self):
        return [
            "__version__ = '%s'" % self.package_dict['version'],
            "__name__ = '%s'" % self.package_dict['name'],
            "__author__ = ['%s']" % self.package_dict['author'],
            "__author_email__ = ['%s']" % self.package_dict['authorMail']
        ]


def command_builder(package_dict):
    cmd_gen = InitCommandGenerator(package_dict)
    init_file = utils.build_cmd_file(cmd_gen.initializer, script_list=[], class_or_def=False)
    init_file = utils.build_cmd_file(cmd_gen.assigner, script_list=init_file, class_or_def=False)
    init_file.append("")
    final_init_file = "\n".join(init_file)
    return final_init_file
