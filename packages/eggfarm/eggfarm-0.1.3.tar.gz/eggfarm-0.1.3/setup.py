# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eggfarm',
 'eggfarm.templates',
 'eggfarm.templates.func',
 'eggfarm.templates.tests']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0', 'MarkupSafe==2.0.1']

entry_points = \
{'console_scripts': ['eggfarm = eggfarm.main:main']}

setup_kwargs = {
    'name': 'eggfarm',
    'version': '0.1.3',
    'description': 'A tool for generating stonewave table function',
    'long_description': 'None',
    'author': 'Yue Ni',
    'author_email': 'niyue.com@gmail.com',
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
