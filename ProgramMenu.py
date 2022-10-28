import random
import os
import colorama
from attrs import define, field, validators
import time
import ctypes
from treelib import Tree


def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)


def do_if_true(thing_to_do, value):
    if value:
        thing_to_do()


# Used in MenuTree
class StopProgram(Exception):
    pass


# Acts as a function to get a Tree object (treelib) of sub_menus of a ProgramMenu object
# (Should be used in a menus get_tree function)
@define
class MenuTree:

    menu_container = field(init=False)
    _coordinates = field(init=False)
    _ids = field(init=False)
    _tree = field(init=False)
    _sub_menu_keeper = field(init=False)
    _current_id = field(init=False)

    def set_values_to_default(self):
        self._ids = [0]  # 0, it's gonna be the identifier for the parent node
        self._tree = Tree()
        self._sub_menu_keeper = []
        self._coordinates = []
        self._current_id = 1

    def get_new_id(self):
        to_return = str(self._current_id)
        self._current_id += 1
        return to_return

    def __attrs_post_init__(self):
        self.set_values_to_default()

    # This is just an algorithm that I made to get a treelib Tree() object based on the sub_menus attributes
    # And its derived attributes from a single menu object (Giving in the begginining of the class)
    # I don't know if this algo has a name, I honestly just came up with it, if you know the name of it please tell me
    # I will add it.

    def zero_step(self):
        last_menu = self._sub_menu_keeper[-1]
        new_menu = last_menu.sub_menus[0]
        self._sub_menu_keeper.append(new_menu)

        id_ = self.get_new_id()
        self._tree.create_node(identifier=id_, parent=self._ids[-1], data=new_menu)

        self._coordinates.append(0)
        self._ids.append(id_)

    def back_incrementer(self, debug=False):
        self._ids.pop()
        self._sub_menu_keeper.pop()

        last_coordinate = self._coordinates[-1]
        last_coordinate += 1

        try:
            new_menu = self._sub_menu_keeper[-1].sub_menus[last_coordinate]
            self._sub_menu_keeper.append(new_menu)
            self._coordinates.append(last_coordinate)

            id_ = self.get_new_id()
            self._tree.create_node(identifier=id_, parent=self._ids[-1], data=new_menu)
            self._ids.append(id_)

        except IndexError:
            if debug:
                print("Index error happened")
            if self._ids[-1] == 0:
                raise StopProgram

            else:
                self._coordinates.pop()
                self.back_incrementer(debug)

    # if you would like to succesfuly use this, I'd highly recommend you to 1.- simplify ProgramMenu's class repr to
    # its tree_identifier only
    # or 2.- straight up disable it, check attrs documentation for more info
    def _debug_get_tree(self):
        self._sub_menu_keeper = [self.menu_container]
        self._tree.create_node(identifier=0, data=self.menu_container)
        print(f"Starting: Sub_menu: {self._sub_menu_keeper}, IDS: {self._ids}, Coordinates: {self._coordinates}")
        while True:
            print("Cycle")
            try:
                print("Step")
                self.zero_step()
            except IndexError:
                print("Back incrementer")
                try:
                    self.back_incrementer(True)
                except StopProgram:
                    break

            print(f"Ending: Sub_menu: {self._sub_menu_keeper}, IDS: {self._ids}, Coordinates: {self._coordinates}")

        return_tree = self._tree
        self.set_values_to_default()
        return return_tree

    def get_tree(self):
        self._sub_menu_keeper = [self.menu_container]
        self._tree.create_node(identifier=0, data=self.menu_container)
        while True:
            try:
                self.zero_step()
            except IndexError:
                try:
                    self.back_incrementer()
                except StopProgram:
                    break
        return_tree = self._tree
        self.set_values_to_default()
        return return_tree


# These should only be instantiated through MenuConfig's 'create' method
@define
class ProgramMenu:
    menu_tree_object = MenuTree()
    instructions = field()
    sub_menus = field(validator=validators.instance_of(list))
    id_ = field(validator=validators.instance_of((str, type(None))))
    menu_config = field()

    @instructions.validator
    def validate_instructions(self, attr, value):
        if len(value) == 0:
            raise ValueError("Instructions should not be empty")

    def evolve_config(self, **kwargs):
        self.menu_config = self.menu_config.evolve_config(**kwargs)

    # prints the menu which each instruction.text indexed
    def print_instructions_text(self):
        final_text = ""
        for index, valor in enumerate(self.instructions):
            final_text += f"[{index}] {valor.text}\n"

        print(final_text)

    def get_str_enumerated_instructions(self):
        return [str(x) for x in range(0, len(self.instructions))]

    # returns an option from all_instruction, based on the chosen instruction
    def return_chosen_instruction(self, number):
        return self.instructions[int(number)]

    def print_titles(self):
        do_if_true(lambda: print(self.menu_config.title_color + self.menu_config.big_title + "\n"),
                   self.menu_config.big_title)
        do_if_true(lambda: print(random.choice(self.menu_config.subtitles) + "\n"), self.menu_config.subtitles)

    def error_msg(self, error_msg, awaiting_time, msg_color):
        self.print_titles()
        print(msg_color + error_msg)
        time.sleep(awaiting_time)
        os.system('cls')
        return True

    # it will print the menu indefinitely, until a valid option is thrown
    def print_until_valid_cls(self, error_awaiting_time=3):
        assert isinstance(error_awaiting_time, (float, int)), f"{error_awaiting_time} is not the correct dt"

        # prints the sets of options and ask for input
        # if the option is not what is desired it gets looped. Until the option its desired
        while True:
            # gets input
            self.print_titles()  # prints titles
            self.print_instructions_text()  # prints the lists of instructions
            chosen_option = input(f"{self.menu_config.menu_election_msg}: ")  # saves input
            os.system('cls')  # cls

            # if it's a desired option then it'll get assigned and the loop breaks
            if chosen_option in self.get_str_enumerated_instructions():
                return self.instructions[int(chosen_option)]

            # else it shows the temperrorscreen and the loops repeats
            else:
                self.error_msg(self.menu_config.menu_wrong_option, 3, colorama.Fore.RED)

    def start(self):
        # If you got all up to the way here likely an exception ocurred within a callable you provided
        set_console_title(self.menu_config.program_title)
        self.print_until_valid_cls().function()

    def start_loop(self):
        set_console_title(self.menu_config.program_title)
        while True:
            chosen_instr = self.print_until_valid_cls()
            if chosen_instr.is_outside_loop:
                break
            chosen_instr.function()

        chosen_instr.function()

    def get_tree(self):
        self.menu_tree_object.menu_container = self
        return self.menu_tree_object.get_tree()
