from typing import NamedTuple, TYPE_CHECKING
from enum import IntEnum

from BaseClasses import ItemClassification as IC

from .subclasses import GSTBSItem

if TYPE_CHECKING:
    from . import GSTBSWorld


class GSTBSItemType(IntEnum):
    basic = 1


# A named tuple is used here as there should never be any need to edit the item data
class GSTBSItemData(NamedTuple):
    name: str
    classification: IC
    count: int
    type: GSTBSItemType = GSTBSItemType.basic


# storing the item data directly in python is the most efficient way for AP worlds
item_data_table: dict[int, GSTBSItemData] = {}  # TODO Set up jinja

item_name_to_id: dict[str, int] = {data.name: address for address, data in item_data_table.items()}


def create_item(world: "GSTBSWorld", name: str) -> GSTBSItem:
    address: int = item_name_to_id[name]
    return GSTBSItem(name, item_data_table[address].classification, address, world.player)


def create_items(world: "GSTBSWorld") -> None:
    # A straight call to the GSTBSItem constructor is faster here than having to immediately find the address again
    # Also, nested list comprehension goes brr
    world.multiworld.itempool += [GSTBSItem(data.name, item_data_table[addr].classification, addr, world.player)
                                  for addr, data in item_data_table.items()
                                  for _ in range(data.count)]
