import gc
from pathlib import Path
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from worlds.AutoWorld import World


def draw_puml(world: "World", path: Path) -> None:
    """ Given a World object this will generate a PUML file at the given path. Use this to visually debug rules

    Taken from https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#setting-rules.
    Options can be seen at the docstring in the definition of `visualize_regions()`

    :param world: world object to be analyzed
    :param path: desired location for the PUML file
    """
    from Utils import visualize_regions
    state = world.multiworld.get_all_state(False, allow_partial_entrances=True)
    state.update_reachable_regions(world.player)
    visualize_regions(world.get_region("Menu"), str(path),
                      show_entrance_names=True, show_locations=True,
                      show_other_regions=True,
                      regions_to_highlight=state.reachable_regions[world.player])


def print_referrers(obj: Any, label: str = "gc_referrers",
                    pretty_print: bool = True, pretty_print_char: str = "+") -> None:
    """ Prints a modules referrers to console output

    :param obj: object to analyze with python's `gc.getreferrers()`
    :param label: section header for the pretty printed output
    :param pretty_print: whether or not to pretty print the output
    """
    # a newline is always necessary so that it doesn't print in-line with test logging
    if pretty_print and len(pretty_print_char) == 1:
        header: str = f"{pretty_print_char * 5} {label} {pretty_print_char * 5}"
        footer: str = f"{12 + len(label)}"
        # the formatting of the dividers is a bit hardcoded for now, but thats alright
        print(f"\n{header}\n{gc.get_referrers(obj)}\n{footer}")
        return
    if len(pretty_print_char) != 1:
        print("\nThe string provided is more than one character long. defaulting to basic print")
    print(f"\n{gc.get_referrers(obj)}")
    return
