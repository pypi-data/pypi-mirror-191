from textwrap import fill

from python_simple_menu import Menu
from python_simple_menu.items import FunctionItem
from python_simple_menu.items import MenuItem


def main():
    main_menu = Menu(prompt="Contents")
    main_menu.items.append(FunctionItem("Preface", __preface))

    ch1_menu = Menu(
        parent=main_menu,
        prompt="Chapter 1: It Begins",
        prompt_go_back="Contents",
        prompt_quit="Good night!",
    )

    ch1_menu.items.append(FunctionItem("Close to Home", __ch1_close_to_home))
    ch1_menu.items.append(FunctionItem("Far Far Away", __ch1_far_far_away))
    main_menu.items.append(MenuItem(ch1_menu))
    main_menu.run()


def __print(text: str):
    print(fill(text, 70))


def __preface():
    __print(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do; eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut; enim ad minim veniam, quis nostrud exercitation ullamco laboris; nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat; nulla pariatur. Excepteur sint occaecat cupidatat non proident,; sunt in culpa qui officia deserunt mollit anim id est laborum."
    )


def __ch1_close_to_home():
    __print(
        "Ullamcorper eget nulla facilisi etiam. Cras fermentum odio eu feugiat pretium. Phasellus faucibus scelerisque eleifend donec pretium vulputate sapien nec sagittis. Turpis nunc eget lorem dolor sed viverra ipsum nunc aliquet. Erat pellentesque adipiscing commodo elit at imperdiet dui accumsan sit. Tristique senectus et netus et malesuada. In iaculis nunc sed augue lacus viverra vitae congue. Leo vel fringilla est ullamcorper. ",
    )


def __ch1_far_far_away():
    __print(
        "Maecenas volutpat blandit aliquam etiam erat velit scelerisque in. Curabitur gravida arcu ac tortor dignissim convallis aenean. Sem fringilla ut morbi tincidunt augue interdum velit euismod. Sollicitudin aliquam ultrices sagittis orci a scelerisque purus semper. Ullamcorper malesuada proin libero nunc consequat. Mauris sit amet massa vitae tortor condimentum. Elementum facilisis leo vel fringilla.",
    )


if __name__ == "__main__":
    main()
