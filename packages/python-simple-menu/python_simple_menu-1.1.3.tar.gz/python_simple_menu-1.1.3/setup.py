# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_simple_menu']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-simple-menu',
    'version': '1.1.3',
    'description': 'Yet another simple console menu',
    'long_description': '# Simple Menu\n\nA lightweight console menu package for python applications. No frills, no fuss.\n\n## Installing\n\nTo install to your project, run the following command:\n\n```commandline\npip install simple_menu\n```\n\n## How to Use\n\n```python\ndef main():\n\t# Create a main menu\n\tm = Menu(prompt="Main Menu")\n\tm.items.append(FunctionItem(label="Item 1", function=lambda: print("Item 1")))\n\n\t# Create a sub-menu\n\tm2 = Menu(parent=m, prompt="Sub Menu 1")\n\tm2.items.append(FunctionItem(label="Item 2", function=lambda: print("Item 2")))\n\n\t# Add the sub-menu to the main menu\n\tm.items.append(MenuItem(label="Sub Menu 1", menu=m2))\n\n\t# Run the menu\n\tm.run()\n\n\nif __name__ == "__main__":\n\tmain()\n\n```\n\nThe menu will run until the user chooses the Quit item, which will exit the application.\nWhen entering a sub-menu, an additional "go back" option is added which will return the\nuser to the parent menu. The various prompts can be customized in the Menu()\nconstructor.\n',
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
