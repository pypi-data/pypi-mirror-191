# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_simple_menu', 'python_simple_menu.examples']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-simple-menu',
    'version': '1.1.12',
    'description': 'Yet another simple console menu',
    'long_description': '# python-simple-menu\n\nA lightweight console menu package for python applications. No frills, no fuss.\n\n## Installing\n\nTo install to your project, run the following command:\n\n```shell\npip install python_simple_menu\n```\n\n## How to use\n\n```python\ndef main():\n    main_menu = Menu(prompt="Main Menu")\n    main_menu.items.append(FunctionItem("Item 1", __item1))\n    main_menu.items.append(FunctionItem("Item 2", __item2))\n    \n    sub_menu1 = Menu(prompt="Sub-Menu 1", parent=main_menu)\n    sub_menu1.items.append(FunctionItem("Item 1", __item1))\n    sub_menu1.items.append(FunctionItem("Item 2", __item2))\n    \n    main_menu.items.append(MenuItem(sub_menu1))    \n    main_menu.run()\n\ndef __item1():\n    print(\'lorem ipsum...\')\n\ndef __item2():\n    print(\'dolor sit amet...\')\n```\n\nThe menu will run until the user chooses Quit ("Q"), which will exit the\napplication. If the menu has a parent menu, an additional Back ("B") option\nwill be rendered which will return the user to the parent menu.\n\nSee the `python_simple_menu/examples` directory for other usages.\n',
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
