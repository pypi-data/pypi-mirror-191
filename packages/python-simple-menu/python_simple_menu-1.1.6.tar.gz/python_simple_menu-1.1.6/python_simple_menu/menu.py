from typing import List
from typing import Optional


class Menu:
    """
    Display a list of choices until the user chooses quit

    Example usage::

                                                                                                                                    from simple_menu.items import FunctionItem
                                                                                                                                    from simple_menu.items import MenuItem
                                                                                                                                    from simple_menu import Menu

                                                                                                                                    m = Menu(prompt="Main Menu")
                                                                                                                                    m.items.append(FunctionItem(label="Item 1", function=lambda: print("Item 2")))

                                                                                                                                    m2 = Menu(parent=m, prompt="Sub Menu 1")
                                                                                                                                    m2.items.append(FunctionItem(label="Item 2", function=lambda: print("Item 2")))
                                                                                                                                    m.items.append(MenuItem(label="Sub Menu 1", menu=m2))

                                                                                                                                    m.run()

    Attributes:

                                                                                                                                    prompt(str): The prompt before the item list (default: "Menu")
                                                                                                                                    prompt_quit(str): The prompt to quit the application (default: "Quit")
                                                                                                                                    prompt_go_back(str): The prompt to exit the sub-menu (default: "Back")
                                                                                                                                    parent(Menu|None): The parent menu this menu belongs to
    """

    def __init__(
        self,
        prompt="Menu",
        prompt_quit: Optional[str] = None,
        prompt_go_back: Optional[str] = None,
        parent: Optional["Menu"] = None,
    ):
        from .items import BaseItem

        if prompt_go_back is None:
            prompt_go_back = parent.prompt if parent else "Back"

        if prompt_quit is None:
            prompt_quit = parent.prompt_quit if parent else "Quit"

        self.prompt = prompt
        self.prompt_quit = prompt_quit
        self.prompt_go_back = prompt_go_back
        self.items: List[BaseItem] = []
        self.parent = parent

    def run(self):

        while True:
            print(self.prompt)

            # render each menu item
            for index, item in enumerate(self.items, start=1):
                print(f" {index}: {item.label}")

            # render "go back" prompt
            if self.parent:
                print(f" B: {self.prompt_go_back}")

            # render "quit" prompt
            print(f" Q: {self.prompt_quit}")

            try:
                choice = input("> ").strip()

                # go back to parent menu
                if choice.upper() == "B" and self.parent:
                    break

                # exit the application
                if choice.upper() == "Q":
                    exit(0)

                # execute the chosen item
                index = int(choice) - 1
                self.items[index].exec()
                continue

            except IndexError:
                print(f"Invalid choice. Try again.")

            except Exception as e:
                print(f"Error: {e}")
                continue
