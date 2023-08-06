# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schemaorg_types']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'schemaorg-types',
    'version': '0.4.0',
    'description': 'Pydantic classes for Schema.org.',
    'long_description': "# schemaorg_types\n [![](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) ![t](https://img.shields.io/badge/status-stable-green.svg) \n\nAn implementation of [Schema.org](https://schema.org) types in [pydantic](https://pydantic-docs.helpmanual.io/)! <br> <br>\n\n## TODO \nI'll update this soon\n\n- docs build\n- release pipeline\n- commit hooks\n- tox, black, pyest, coverage, isort configs\n- testing against schema.org",
    'author': 'Adam Ulring',
    'author_email': 'adam.ulring1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
