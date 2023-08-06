# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dtuhpc',
 'dtuhpc.cli',
 'dtuhpc.cli.commands',
 'dtuhpc.cli.commands.server',
 'dtuhpc.commands',
 'dtuhpc.jobwriter',
 'dtuhpc.jobwriter.commands',
 'dtuhpc.jobwriter.options']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=39.0.1,<40.0.0',
 'fabric>=2.7.0,<3.0.0',
 'gitpython>=3.1.30,<4.0.0',
 'pygithub>=1.57,<2.0',
 'python-semantic-release>=7.33.1,<8.0.0',
 'rich>=13.2.0,<14.0.0',
 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['dtuhpc = dtuhpc.cli.cli:main']}

setup_kwargs = {
    'name': 'dtuhpc',
    'version': '1.0.10',
    'description': '',
    'long_description': '# DTU HPC',
    'author': 'Jonas Hoffmannn',
    'author_email': 's204071@student.dtu.dk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
