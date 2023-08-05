# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colorutil']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.56.4,<0.57.0', 'numpy>=1.21.6,<2.0.0']

setup_kwargs = {
    'name': 'colorutil',
    'version': '0.9.1',
    'description': '',
    'long_description': '',
    'author': 'Simon Warchol',
    'author_email': 'simonwarchol@g.harvard.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/simonwarchol/colorutil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
