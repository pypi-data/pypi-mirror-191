import os

from .command import Command


class RunCommand(Command):
    """
        Run scripts
    """

    def __init__(self,  params: dict = None):
        self.params = params if params else {'script': 'main'}
        super().__init__()

    def run(self):
        """
            run scripts
        """
        script = self.params.get('script')
        
        if script == 'main':
            run_script = self.config.get('main')
            os.system('python ' + run_script)
        else:
            run_script = self.config.get('scripts').get(script)

        if run_script:
            os.system(run_script)
        else:
            raise NotImplementedError(f'command { script } not found')
