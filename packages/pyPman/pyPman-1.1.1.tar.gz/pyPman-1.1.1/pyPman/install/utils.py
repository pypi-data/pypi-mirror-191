class CommandInitializer(object):
    def __init__(self, pkg_dict):
        self.package_dict = pkg_dict

    @property
    def initializer(self):
        return [
            "# This project is build with %s %sV" % (self.package_dict['name'], self.package_dict['version']),
            "# Please don't edit without knowing much about the working project",
            "# If you have any queries about python project builder,",
            "# Please contact below person(s)\n# %s - %s" % (
                self.package_dict['author'], self.package_dict['authorMail']
            )
        ]
