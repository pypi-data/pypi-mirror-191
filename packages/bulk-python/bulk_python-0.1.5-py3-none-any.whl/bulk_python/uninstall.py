import os
from .command import Command


class UninstallCommand(Command):
    """
        uninstall a single package or all
    """

    def __init__(self, packages: list | None = None) -> None:
        self.packages = packages

        super().__init__()

    def run(self):
        if not self.packages:
            self.packages = dict.keys(self.config['dependencies'])

        if len(self.packages) > 0:
            os.system('pip uninstall ' + ' '.join(self.packages))

        for package in self.packages:
            if package in self.config['dependencies']:
                del self.config['dependencies'][package]

        self.replace_config()
