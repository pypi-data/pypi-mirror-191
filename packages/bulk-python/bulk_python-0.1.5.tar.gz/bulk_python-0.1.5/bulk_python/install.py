import os
import pkg_resources

from pathlib import Path

from .command import Command


class InstallCommand(Command):
    """
        Install command create a bulk.json file,
        if a  bulk.json file is not found in project we try installing from requirements.txt
    """

    def __init__(self, options: list, params: dict = None):
        self.options = options
        self.params = params

        super().__init__()

    def parse_version(self, version: str):
        """
            parse version prefix
        """
        return '>=' + version.removeprefix('^') if version.startswith('^') else '==' + version

    def install(self, package: str):
        """
            Install package
        """
        os.system('pip install ' + package)

    def lock(self, can_install=False, ancestor='bulk'):
        """
            Reset config dependencies, add or update dependencies
        """
        if ancestor == 'pip' or can_install:
            if not Path('requirements.txt').exists():
                os.system('pip freeze > requirements.txt')

            with open('requirements.txt', 'rb') as file:
                packages = {}
                requirements = file.readlines()
                requirements = list(
                    map(lambda requirement: requirement.decode().strip(), requirements))

                if can_install:
                    self.install(' '.join(requirements))

                for requirement in requirements:
                    name, version = requirement.split('==')
                    packages[name] = version
                file.close()
                self.config['dependencies'] = packages

        self.replace_config()

    def run(self):
        """
            run middleware
        """

        if '--install-all' in self.options:
            dependencies = self.config.get('dependencies')

            def map_dependencies(key: str):
                version = dependencies.get(key)
                return f"{ key }{ '' if version == '@latest' or len(version.strip()) == 0 else self.parse_version(version) }"

            if len(dict.keys(dependencies)) > 0:
                packages = list(map(map_dependencies, dict.keys(dependencies)))
                packages = ' '.join(packages)
                self.install(packages)
            else:
                return self.lock(True)

        if '--install-single' in self.options and self.params:
            package = self.params.get('package')
            self.install(package)
            for package in package.split(' '):
                self.config['dependencies'][package] = pkg_resources.get_distribution(package).version
                self.replace_config()
            
        if '--dry' in self.options:
            self.lock()
