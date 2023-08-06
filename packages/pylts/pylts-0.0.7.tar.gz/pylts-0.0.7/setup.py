# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylts']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pydantic>=1.10.4,<2.0.0',
 'python-dotenv>=0.21,<0.22']

setup_kwargs = {
    'name': 'pylts',
    'version': '0.0.7',
    'description': 'Pydantic wrapper around litestreamed database specific to an AWS bucket.',
    'long_description': '# pylts\n\n![Github CI](https://github.com/justmars/pylts/actions/workflows/main.yml/badge.svg)\n\nPydantic wrapper around litestreamed database specific to an AWS bucket.\n\n## Development\n\nSee [documentation](https://justmars.github.io/pylts).\n\n1. Run `poetry shell`\n2. Run `poetry update`\n3. Run `pytest`\n',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://mv3.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
