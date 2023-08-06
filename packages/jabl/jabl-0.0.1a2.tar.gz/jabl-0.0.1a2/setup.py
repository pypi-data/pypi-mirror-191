# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jabl']

package_data = \
{'': ['*']}

install_requires = \
['beartype>=0.12,<0.13']

setup_kwargs = {
    'name': 'jabl',
    'version': '0.0.1a2',
    'description': 'An attempt to make lists in Python more useful, functional, and fun to use.',
    'long_description': "# just-a-better-list\nLet's make python lists a bit more fun and intuitive to use, shall we?\n",
    'author': 'Nic Harvey',
    'author_email': 'nicharvey@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
