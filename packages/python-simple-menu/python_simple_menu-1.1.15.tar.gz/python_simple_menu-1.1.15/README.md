# python-simple-menu

A lightweight console menu package for python applications. No frills, no fuss.

## Installing

To install to your project, run the following command:

```shell
pip install python_simple_menu
```

## How to use

```python
def main():
    main_menu = Menu(prompt="Main Menu")
    main_menu.items.append(FunctionItem("Item 1", __item1))
    main_menu.items.append(FunctionItem("Item 2", __item2))
    
    sub_menu1 = Menu(prompt="Sub-Menu 1", parent=main_menu)
    sub_menu1.items.append(FunctionItem("Item 1", __item1))
    sub_menu1.items.append(FunctionItem("Item 2", __item2))
    
    main_menu.items.append(MenuItem(sub_menu1))    
    main_menu.run()

def __item1():
    print('lorem ipsum...')

def __item2():
    print('dolor sit amet...')
```

The menu will run until the user chooses Quit ("Q"), which will exit the
application. If the menu has a parent menu, an additional Back ("B") option
will be rendered which will return the user to the parent menu.

See the `python_simple_menu/examples` directory for other usages.
