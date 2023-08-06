from .command import Command
from .install import InstallCommand


class InitCommand(Command):
    """
        Init bulk in project
    """

    def __init__(self, params: dict = None):
        self.params = params if params else {'ancestor': 'bulk'}

        super().__init__()

    def run(self):
        return InstallCommand(options=[]).lock(ancestor=self.params.get('ancestor'))
