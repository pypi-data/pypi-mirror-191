from pyPman.install import utils as install_utils
from pyPman.utilities import utils


class CommandGenerator(install_utils.CommandInitializer):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def license_creator(self):
        default_license = ""
        main_license = None
        if self.package_dict['license'] == "GNU V3":
            main_license = default_license
        else:
            # TODO: Later options may provide the license availability for other licenses
            print("Please copy your license in 'LICENSE' file if available")
        return [
            "%s" % main_license
        ]


def command_builder(package_dict):
    cmd_gen = CommandGenerator(package_dict)
    main_file = utils.build_cmd_file(cmd_gen.initializer, class_or_def=False)
    main_file = utils.build_cmd_file(cmd_gen.readme_creator, script_list=main_file)
    main_file.append("")
    return "\n".join(main_file)