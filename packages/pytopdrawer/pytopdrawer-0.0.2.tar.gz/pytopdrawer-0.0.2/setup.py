# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytopdrawer']

package_data = \
{'': ['*']}

install_requires = \
['smpl', 'uncertainties']

entry_points = \
{'console_scripts': ['hepi-fast = pytopdrawer.pytopdrawer:main']}

setup_kwargs = {
    'name': 'pytopdrawer',
    'version': '0.0.2',
    'description': 'Plot top files with python and matplotlib (mainly from POWHEG)',
    'long_description': '# pytopdrawer\n\nThis project plots .top files.',
    'author': 'Alexander Puck Neuwirth',
    'author_email': 'alexander@neuwirth-informatik.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/APN-Pucky/pytopdrawer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
