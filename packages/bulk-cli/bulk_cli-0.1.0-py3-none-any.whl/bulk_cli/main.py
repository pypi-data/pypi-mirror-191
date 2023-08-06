import sys

from .run import RunCommand
from .init import InitCommand
from .help import HelpCommand
from .install import InstallCommand
from .uninstall import UninstallCommand


def commands(argv: list):
    """
        use  argparser instead of hardcoded values
    """

    if 'install' in argv:
        if len(argv) > 1:
            if argv[1] == '--dry':
                return InstallCommand(['--dry'])
            else:
                return InstallCommand(['--install-single'], {'package': ' '.join(argv[1:]) })
        else:
            return InstallCommand(['--install-all'])
    elif 'run' in argv:
        if len(argv) > 1:
            return RunCommand({'script': argv[1]})
        else:
            return RunCommand()
    elif 'init' in argv:
        if '--ancestor=pip' in argv:
            return InitCommand({'ancestor': 'pip'})
        else:
            return InitCommand()
    elif 'uninstall' in argv:
        if len(argv) > 1:
            return UninstallCommand(argv[1:])
        else:
            return UninstallCommand()
    else:
        return HelpCommand()


def cli(args: list | None = None):
    """
        main application function
    """
    if not args:
        args = sys.argv

    command = commands(args[1:])
    if command:
        command.run()


if __name__ == '__main__':
    cli()
