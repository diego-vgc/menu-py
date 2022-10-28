![made with love](https://img.shields.io/badge/Made_with-<3-red)
# Setup
### Firstly, install the required libraries that are in requirements.txt, then by putting both menu_py.py and ProgramMenu.py in the same folder, theorically everything should be okay, however, I have not tested it that way, I would recommend to keep both files in the main project folder (within the script file, preferably)


# Basic Usage
```python
import time
from menu_py import MenuConfig

# Warning: All menu instances should be instantiated from a MenuConfig object 'create' method
# (Like its done in this example)


def print_something(something):
    print(something)
    time.sleep(1)


# Default values are being used in this config.
a_config = MenuConfig()
my_menu = a_config.create(
    # Add tuples with a string, and a callable, and you will have your instructions set up
    ("Print wow", lambda: print_something("wow")),
    ("Print stephen", lambda: print_something("Stephen"))
)

my_menu.start()
# (run this)
```
## Loop menus
```python
# If you would like to stop the loop before the callable is run,
# just add a third position parameter as 'True' to the tuple, this parameter is called 'is_outside_loop',
# that name is only for demonstration though

# ++Note that setting it to False is useless, as it is already False by default


a_config = MenuConfig()
my_menu = a_config.create(
    ("Print wow", lambda: print_something("wow"), True),
    ("Print stephen", lambda: print_something("Stephen"))
)

# To run these loops do start_loop instead of start
# Keep in mind that if you run the start method, all is_outside_loop parameters will be ignored
my_menu.start_loop()
# (run this)
```
### By the way, most procedures are NOT thread safe, but, if you use either just start() or a instruction with is_outside_loop factor set to True, no harm is going to happen to any callables you assign, as the menu proccess will stop right before running your callable

# Customize your configs
### Here is a list of all the parameters that you can add to your config
- `program_title` The title of the command prompt (str)
- `big_title` A title that is going to be displayed, I recommend an ascii-style (str)
- `title_color` The color of big_title (use colorama.Fore, and its associated)
- `menu_wrong_option` The error message that is gonna be displayed when a wrong option is selected (str)
- `menu_election_msg` The message that is gonna be displayed when asking for input (list)
- `subtitles` A list of strings, each time a menu is shown, a random of these is gonna be shown, if you don't add this parameter, no subtitles will ever be shown (list)
### Example:
```python
import time
import colorama
from menu_py import MenuConfig


def print_something(something):
    print(something)
    time.sleep(1)


a_config = MenuConfig(subtitles=["Hey, this is me", "Also try terraria!"])
a_config.big_title = """
 _   _      _ _         _    _            _     _ 
| | | |    | | |       | |  | |          | |   | |
| |_| | ___| | | ___   | |  | | ___  _ __| | __| |
|  _  |/ _ \ | |/ _ \  | |/\| |/ _ \| '__| |/ _` |
| | | |  __/ | | (_) | \  /\  / (_) | |  | | (_| |
\_| |_/\___|_|_|\___/   \/  \/ \___/|_|  |_|\__,_|                                                                                       
"""
a_config.title_color = colorama.Fore.BLUE

my_menu = a_config.create(
    ("Print wow", lambda: print_something("wow"), True),
)

# If you want the color setup to run correctly, please initialize colorama this way
colorama.init(autoreset=True)
my_menu.start()
colorama.deinit()
# (run this)
```
## Evolve config from a menu
```python
from menu_py import MenuConfig
import time


def print_something(something):
    print(something)
    time.sleep(1)


my_config = MenuConfig()
my_config = MenuConfig(subtitles=["Hey, this is me", "Also try terraria!"])

menu = my_config.create(("Print wow", lambda: print_something("wow"), True))
menu.evolve_config(subtitles=["Why always me :("])

menu.start()
```
# Create your own error screens
```python
from menu_py import MenuConfig
import colorama
import time


def print_something(something):
    print(something)
    time.sleep(1)


my_config = MenuConfig()

my_config = MenuConfig(subtitles=["Hey, this is me", "Also try terraria!"])
my_config.big_title = """
 _   _      _ _         _    _            _     _ 
| | | |    | | |       | |  | |          | |   | |
| |_| | ___| | | ___   | |  | | ___  _ __| | __| |
|  _  |/ _ \ | |/ _ \  | |/\| |/ _ \| '__| |/ _` |
| | | |  __/ | | (_) | \  /\  / (_) | |  | | (_| |
\_| |_/\___|_|_|\___/   \/  \/ \___/|_|  |_|\__,_|                                                                                       
"""
my_config.title_color = colorama.Fore.BLUE
menu = my_config.create(("Print wow", lambda: print_something("wow"), True))
colorama.init(autoreset=True)
# Awaiting time = time sleep before cleaning the screen
menu.error_msg(error_msg="You did something wrong!", awaiting_time=3, msg_color=colorama.Fore.RED)
colorama.deinit()
# (run this)
```

# Tree View
```python
from menu_py import MenuConfig
import time

# You can also create a Tree of the sub_menus that you'd like!
# Thanks to the powerful treelib library :)


def print_something(something):
    print(something)
    time.sleep(1)


default_config = MenuConfig()

# You need to specify in each menu:
# 1.- it's submenus
# 2.- 'id_', as for a string identifier (optional, but recommended)

fourth_menu = default_config.create(("Print adios", lambda: print_something("Adios world!")),
                                    id_="Adios")
third_menu = default_config.create(("Print congrats", lambda: print_something("Congrats world!")),
                                   id_="Congrats", sub_menus=fourth_menu)
second_menu = default_config.create(("Print bye", lambda: print_something("Bye world!")),
                                    id_="Bye")
first_menu = default_config.create(("Print hello", lambda: print_something("Hello world!")),
                                   id_="Hello", sub_menus=[second_menu, third_menu])

tree_ = first_menu.get_tree()
tree_.show(data_property="id_")

# Note that this is a Tree object from treelib, each node has all of its menu properties attached in
# You can filter them with 'data_property', but also there is a ton of more powerful stuff that you can do
# Checkout https://treelib.readthedocs.io/en/ for more information

```
Output:

!["Tree output"](https://i.imgur.com/RkIkQXp.png)
# How to contribute?
### Please use the forking method, see: https://www.dataschool.io/how-to-contribute-on-github/, you might also want to submit an issue, I honestly don't understand how the issue system works, but feel free to submit one if you are able to. For any recommendation just email me at diegovegayt12@gmail.com. I will try my best to add any form of contribution