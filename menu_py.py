import attrs
from attrs import define, field, validators
import colorama
import ProgramMenu


# Class that is used to import tuples as instructions when creating a ProgramMenu object
@define
class MenuInstruction:
    text = field(validator=validators.instance_of(str))
    function = field(validator=validators.is_callable())
    is_outside_loop = field(default=None, validator=validators.instance_of((type(None), bool)))


@define
class MenuConfig:
    program_title = field(validator=validators.instance_of((str, type(None))), default=None)
    title_color = field(validator=validators.in_([colorama.Fore.BLACK, colorama.Fore.RED, colorama.Fore.GREEN,
                                                  colorama.Fore.YELLOW, colorama.Fore.BLUE, colorama.Fore.MAGENTA,
                                                  colorama.Fore.CYAN, colorama.Fore.WHITE]),
                        default=colorama.Fore.WHITE)
    menu_wrong_option = field(validator=validators.instance_of(str), default="You have picked an incorrect option")
    menu_election_msg = field(validator=validators.instance_of(str), default="Please choose an option")

    big_title = field(validator=validators.instance_of((str, type(None))), default=None)
    subtitles = field(validator=validators.instance_of((list, type(None))), default=None)

    def create(self, *args, id_=None, sub_menus=None):
        # Bunch of validators

        if isinstance(sub_menus, ProgramMenu.ProgramMenu):
            sub_menus = [sub_menus]
        elif sub_menus is None:
            sub_menus = []
        for x in sub_menus:
            if not isinstance(x, ProgramMenu.ProgramMenu):
                raise ValueError("sub_menus argument should be a list of ProgramMenu instances")

        instructions = [MenuInstruction(*tup) for tup in args]

        return ProgramMenu.ProgramMenu(instructions, sub_menus, id_, menu_config=self)

    def evolve_config(self, **kwargs):
        return attrs.evolve(inst=self, **kwargs)
