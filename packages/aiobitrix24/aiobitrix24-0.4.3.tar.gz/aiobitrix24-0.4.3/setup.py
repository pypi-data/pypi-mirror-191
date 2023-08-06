# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiobitrix24', 'aiobitrix24.methods']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0']

setup_kwargs = {
    'name': 'aiobitrix24',
    'version': '0.4.3',
    'description': 'Simple async bitrix-24 rest client',
    'long_description': '<h2 align="center">AIOBitrix24</h2>\n\n<p align="center">\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>',
    'author': 'andrpocc',
    'author_email': 'andrey.pochatkov@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/prin-it/bitrix24-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
