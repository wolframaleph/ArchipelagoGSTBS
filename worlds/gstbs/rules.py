from typing import TypedDict, Callable, TYPE_CHECKING

from worlds.generic.Rules import CollectionRule, set_rule, add_rule

if TYPE_CHECKING:
    from BaseClasses import CollectionState
    from . import GSTBSWorld


# There are at least two somewhat different styles for declaring the rules. The subnautica world defines all
# of the rules in functions in `rules.py`, while messenger uses a dictionary of location names and lambdas
# See the rules for messenger and the rules for subnautica for some clear examples


def test_rule(state: "CollectionState", player: int) -> bool:
    # return state.has("Stub Item", player)  # example rule
    return True


def set_rules(world: "GSTBSWorld") -> None:
    player = world.player
    set_rule(world.get_location("Stub Location"), lambda state: test_rule(state, player))
    world.multiworld.completion_condition[player] = lambda state: state.has("Victory!", player)
