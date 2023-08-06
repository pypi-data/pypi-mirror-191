from pyPman.utilities import utils
from pyPman.install import utils as install_utils


class CommandGenerator(install_utils.CommandInitializer):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def readme_creator(self):
        return [
            "# %s" % self.package_dict['name'],
            "%s" % self.package_dict['description']
        ]


def command_builder(package_dict):
    cmd_gen = CommandGenerator(package_dict)
    main_file = utils.build_cmd_file(cmd_gen.initializer, class_or_def=False)
    main_file = utils.build_cmd_file(cmd_gen.readme_creator, script_list=main_file)
    main_file.append("")
    return "\n".join(main_file)
