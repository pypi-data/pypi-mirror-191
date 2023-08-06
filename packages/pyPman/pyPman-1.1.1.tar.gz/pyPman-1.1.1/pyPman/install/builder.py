"""
Build structure:
    projectName
        \____ packageName
        \       \____ __init__.py
        \       \____ __main__.py(entry point)
        \____ README.md
        \____ LICENSE
        \____ setup.py

    By building the project with PyProject manager, you can use the project for installing using 'pip'

"""
import os
from pyPman.install import setup_builder, init_builder, main_builder, readme_builder, license_builder
from pyPman.utilities import utils


def setup_structure(output, package_dict):
    """ Definition to setup the directory and files structure in output folder
    """
    directories = [
        package_dict['name'],
        os.path.join(package_dict['name'], package_dict['package'])
    ]
    user_modules = [os.path.join(
        package_dict['name'],
        package_dict['package'],
        module
    ) for module in package_dict['module']]
    directories.extend(user_modules)

    files = [
        os.path.join(package_dict['name'], "README.md"),
        os.path.join(package_dict['name'], "LICENSE"),
        os.path.join(package_dict['name'], "setup.py"),
        os.path.join(package_dict['name'], os.path.join(package_dict['package'], "__init__.py")),
        os.path.join(package_dict['name'], os.path.join(package_dict['package'], package_dict['main']))
    ]
    user_module_initialise = [os.path.join(module_dir, '__init__.py') for module_dir in user_modules]
    files.extend(user_module_initialise)

    for directory in directories:
        utils.create_directory(output, directory)

    for file_name in files:
        utils.create_file(output, file_name=file_name)

    return files


def install(output, package_dict):
    # Setting up the file structure in the output directory
    script_files = setup_structure(output, package_dict)

    # Generating file scripts
    init_build_file = init_builder.command_builder(package_dict)
    main_build_file = main_builder.command_builder(package_dict)
    setup_build_file = setup_builder.commands(package_dict)
    print("Writing new files to the scripts")
    utils.write_file(script_files[3], data=init_build_file)
    utils.write_file(script_files[4], data=main_build_file)
    utils.write_file(script_files[2], data=setup_build_file)
