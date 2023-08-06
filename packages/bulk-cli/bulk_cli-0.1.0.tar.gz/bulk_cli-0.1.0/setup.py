# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bulk_cli']

package_data = \
{'': ['*'], 'bulk_cli': ['configs/*']}

entry_points = \
{'console_scripts': ['bulk = bulk_cli.main:cli']}

setup_kwargs = {
    'name': 'bulk-cli',
    'version': '0.1.0',
    'description': 'Bulk helps you declare, manage and install dependencies of Python projects.',
    'long_description': '# bulk\nBulk helps you declare, manage and install dependencies of Python projects.\n\n# Installations\ninstall bulk on python using pip\n\n```shell\n    pip install bulk-cli\n```\n\n# Bulk commands\n```shell\n    bulk init\n```\n\ninit bulk config in a project \nif you have an old project using pip use the flag\n``--ancestor=pip`` ( Not necessary if you have requirements.txt in your project)\n\n```shell\nbulk install\n```\n\nIf you have requirements.txt file in your project bulk will add all packages from it to bulk.dependencies \n\n```shell\nbulk install package-name\n```\n\nInstall a package from pip library\n\n```shell\nbulk install --dry\n```\nCreate bulk config from pip packages without installing\n\n```shell\nbulk uninstall\n```\nUninstall project dependencies\n\n```shell\nbulk uninstall package-name\n```\n\nUninstall a package from pip library\n\n\n```shell\nbulk run ...\n```\n\nBulk allows you to run multiple commands one \n\n```json\n    {\n        "script": {\n            "dev": "python manage.py makemigrations && python manage.py migrate && python manage.py runserver"\n        }\n    }\n```\n\nNote: replace && with ; if you are using windows\nrun dev \n```shell\n    bulk run dev\n```\n\n# Documentation\nDocumentation for the current version of Bulk  is available from github README.\n\n\n[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/lyonkvalid)',
    'author': 'Oguntunde Caleb Fiyinfoluwa',
    'author_email': 'oasis.mystre@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
