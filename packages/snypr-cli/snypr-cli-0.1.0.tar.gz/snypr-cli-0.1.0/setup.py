# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omega', 'omega.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'pysigma>=0.6.5,<0.7.0', 'sigmatools>=0.21.0,<0.22.0']

entry_points = \
{'console_scripts': ['snypr-cli = omega.cli.main:main']}

setup_kwargs = {
    'name': 'snypr-cli',
    'version': '0.1.0',
    'description': 'Omega to Spotter Query Convertor',
    'long_description': None,
    'author': 'Rouzbeh Radparvar',
    'author_email': 'rradparvar@securonix.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Securonix/sigma2snypr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
