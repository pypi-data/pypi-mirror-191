import os
import pkg_resources

from .command import Command


class HelpCommand(Command):
    """
        Help command
    """

    def run(self):
        version = pkg_resources.get_distribution('bulk_python').version

        with open(os.path.join(Command.BASE_DIR, 'configs', 'help.txt'), 'rb') as file:
            help_text = file.read().decode(
                'utf-8').replace('{ version }',  version)
            file.close()

        print(help_text)
