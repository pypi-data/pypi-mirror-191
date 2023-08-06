# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ateto']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1,<4.0',
 'beautifulsoup4>=4.1,<5.0',
 'click>=8.1,<9.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28,<3.0',
 'watchdog>=2.2,<3.0',
 'xdg>=5.1,<6.0']

entry_points = \
{'console_scripts': ['ateto = ateto.cli:cli']}

setup_kwargs = {
    'name': 'ateto',
    'version': '0.2.0',
    'description': 'This is a set of tools to write templates outside of Anki.',
    'long_description': 'None',
    'author': 'bisam',
    'author_email': 'bisam@r4.re',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
