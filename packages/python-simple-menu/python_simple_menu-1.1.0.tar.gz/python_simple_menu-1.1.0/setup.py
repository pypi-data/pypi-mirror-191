# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_simple_menu']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-simple-menu',
    'version': '1.1.0',
    'description': '',
    'long_description': '',
    'author': 'Chris Vann',
    'author_email': 'chrisvann01@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
