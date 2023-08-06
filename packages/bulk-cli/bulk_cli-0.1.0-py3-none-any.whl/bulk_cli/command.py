import os
import json
from pathlib import Path


class Command:
    """
        Command Interface
    """
    BASE_DIR = Path(__file__).parent
    BULK_CONFIG_PATH = os.path.join(os.getcwd(), 'bulk.json')
    DEFAULT_CONFIG_PATH = os.path.join(BASE_DIR, 'configs', 'default.json')

    def __init__(self) -> None:
        self.config = self._config()

    @staticmethod
    def _config() -> dict:
        """
            returns project config file or default config
        """
        path = __class__.BULK_CONFIG_PATH if Path(
            __class__.BULK_CONFIG_PATH).exists() else __class__.DEFAULT_CONFIG_PATH

        with open(path, 'rb') as file:
            return json.loads(file.read())

    def replace_config(self):
        """
            update packages
        """
        with open(Command.BULK_CONFIG_PATH, 'wb') as file:
            dependencies: dict = self.config['dependencies']
            self.config['dependencies'] = dict(sorted(dependencies.items()))
            file.write(json.dumps(self.config, indent=4).encode('utf-8'))
            file.close()

    def run(self):
        """
            Your run middleware here
        """
        raise NotImplementedError

    def execute(self):
        """
            command is called
        """
        return self.run()
