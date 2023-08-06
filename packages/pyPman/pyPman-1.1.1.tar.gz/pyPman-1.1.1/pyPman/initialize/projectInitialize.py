import sys
import os as _os
import logging
import pprint
import json

from traVer import Version

log = logging.getLogger(__name__)

PROJECT_NAME = None
PACKAGE_NAME = None
PACKAGE_VERSION = "1.0.0"
DESCRIPTION = None
ENTRY_POINT = "__main__.py"
GIT_REPO = None
KEYWORDS = None
AUTHOR = None
AUTHOR_EMAIL = None
LICENSE = "GNU V3"


def create_files(output, file_name, data=None):
    if not _os.path.exists(output):
        log.error("Please make sure that the output directory exists")
        return False
    file_path = _os.path.join(output, file_name)
    with open(file_path, 'w') as newFile:
        if data and isinstance(data, dict):
            json.dump(data, newFile, indent=2)
        elif data:
            newFile.write(data)
    log.info("%s file created in %s" % (file_name, output))
    return True


def get_project_details(install_path, pkg_file=None):
    package_file = ".%s.json" % (pkg_file or PROJECT_NAME)
    pkg_file_path = _os.path.join(install_path, package_file)
    if check_for_project(install_path, pkg_file=pkg_file):
        with open(pkg_file_path) as fd:
            data = json.load(fd)
        return data


def check_for_project(install_path, pkg_file=None):
    package_file = ".%s.json" % (pkg_file or PROJECT_NAME)
    pkg_file_path = _os.path.join(install_path, package_file)
    if _os.path.exists(pkg_file_path):
        return True
    return False


def init_project(install_path, project=None):
    global PROJECT_NAME, PACKAGE_NAME, PACKAGE_VERSION, DESCRIPTION, ENTRY_POINT, GIT_REPO
    global KEYWORDS, AUTHOR, AUTHOR_EMAIL, LICENSE
    pkg_name = _os.path.basename(install_path)
    package_dict = {}
    if project:
        log.info("Project name set to: %s" % project)
        query_detail("Project Name", default=project, accepted=True)
    PROJECT_NAME = project or query_detail("Project Name", default=pkg_name)
    if check_for_project(install_path):
        package_dict = get_project_details(install_path)
        log.warning("%s already been setup in the directory" % PROJECT_NAME)
    PACKAGE_NAME = query_detail("Package Name", default=PROJECT_NAME)
    PACKAGE_VERSION = query_detail("Project Version", default=package_dict.get('version', None) or PACKAGE_VERSION)
    try:
        pkg_version = Version(PACKAGE_VERSION)
    except Exception as err:
        log.error("%s, Please use semantic versioning syntax i.e., 12.3.4 (or) 2.3.4-beta.5" % err)
        sys.exit()

    DESCRIPTION = query_detail("Description", default=package_dict.get('description', None))
    ENTRY_POINT = query_detail("Entry Point", default=package_dict.get('main', None) or ENTRY_POINT)
    GIT_REPO = query_detail("Git Repository", default=package_dict.get('url', None))
    KEYWORDS = query_detail("Keywords", default=package_dict.get('keywords', None))
    AUTHOR = query_detail("Author", default=package_dict.get('author', None))
    AUTHOR_EMAIL = query_detail("Author Email", default=package_dict.get('authorMail', None))
    LICENSE = query_detail("License", default=package_dict.get('license', None) or LICENSE)

    package_dict = {
        "name": PROJECT_NAME,
        "package": PACKAGE_NAME,
        "version": PACKAGE_VERSION,
        "description": DESCRIPTION,
        "main": ENTRY_POINT,
        "author": AUTHOR,
        "authorMail": AUTHOR_EMAIL,
        "license": LICENSE,
        "url": GIT_REPO,
        "dependency": package_dict.get("dependency", []),
        "module": package_dict.get("module", []),
    }

    log.warning("About to write the following dictionary to <package>.json\n")
    pprint.pprint(package_dict)

    accept = query_detail("Is this Okay?", default="yes")
    if not accept == "yes":
        log.warning("Project creation exited by user.")
        sys.exit()

    create_files(install_path, ".%s.json" % PROJECT_NAME, data=package_dict)
    return package_dict


def query_detail(query, default=None, accepted=False):
    query = query.strip() + ": "
    if default:
        query = query + "(%s) " % default
    if accepted:
        print(query)
        return
    result = input(query)

    if result:
        return result
    else:
        return default
