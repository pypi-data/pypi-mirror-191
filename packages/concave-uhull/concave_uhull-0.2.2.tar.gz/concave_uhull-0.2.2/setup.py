# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['concave_uhull', 'concave_uhull.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0', 'scipy>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'concave-uhull',
    'version': '0.2.2',
    'description': 'A simple (but not simpler) algorithm for concave hull of 2D point sets using an alpha shape algorithm.',
    'long_description': 'concave_uhull*\n--------------\n\nA simple (but not simpler) algorithm for concave hull of 2D point sets using an alpha shape algorithm.\n\nNotes\n-----\n  * uhull! (Brazil) yeah! (expresses joy or celebration)\n\nHomepage\n--------\n* `Project Homepage <https://luanleonardo.github.io/concave_uhull/>`_\n',
    'author': 'Luan',
    'author_email': 'llvdmoraes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://luanleonardo.github.io/concave_uhull/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)
