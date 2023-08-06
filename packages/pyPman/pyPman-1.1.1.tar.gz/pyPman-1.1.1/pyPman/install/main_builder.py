from pyPman.utilities import utils
from pyPman.install import utils as install_utils


class MainCommandGenerator(install_utils.CommandInitializer):
    def __init__(self, *args):
        super(MainCommandGenerator, self).__init__(*args)

    @property
    def cli_creator(self):
        return [
            "def cli():",
            "   # Add your code here to run the command line interface",
            "   print('Command line interface will exit after displaying this message.')",
            "   print('If you want to edit, go to <projectName>/<packageName>/__main__.py')",
            "",
            "",
            "def cli_ui():",
            "   # Add your code here to run the command line interface",
            "   pass"

        ]


def command_builder(package_dict):
    cmd_gen = MainCommandGenerator(package_dict)
    main_file = utils.build_cmd_file(cmd_gen.initializer, script_list=[], class_or_def=False)
    main_file = utils.build_cmd_file(cmd_gen.cli_creator, script_list=main_file)
    main_file.append("")
    final_main_file = "\n".join(main_file)
    return final_main_file
