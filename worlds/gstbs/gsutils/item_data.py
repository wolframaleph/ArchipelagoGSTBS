# Ported from https://github.com/Karanum/gs2-randomiser2/blob/master/randomiser/game_data/items.js

import struct
import pickle
from dataclasses import dataclass
from typing import TYPE_CHECKING
import orjson

from .binary_utils import Rom, ITEM_STRUCT_FMT
from .text_utils import read_line, format_line, GSTBSInternalStringData

if TYPE_CHECKING:
    from pathlib import Path

_ITEM_TABLE_OFFSET: int = 0x7B6A8
_ITEM_TABLE_LEN: int = 269
_ITEM_STRUCT_LEN: int = 44
_ITEM_NAME_OFFSET: int = 386
_ITEM_DESC_OFFSET: int = 117


@dataclass
class GSTBSInternalItemData:
    id : int  # this is technically also an index. The dict key for each item will be str(id)
    name : str
    desc : str
    addr : int
    cost : int
    item_type : int
    flags : int
    equip_compat : int
    # icon : int  # NOTE is this an address? or an id?
    attack : int
    defense : int
    unleash_rate : int
    use_type : int
    unleash_id : int
    # attribute : int  # NOTE attribute might be able to be randomized later?
    use_effect : int  # moved up so that the equip effects array is last in the .json
    equip_effects : list[list[int]]

    def pack(self):
        raise NotImplementedError  # will be needed for patching the rom


def read_item(rom: Rom, id_: int, name: str, desc: str) -> GSTBSInternalItemData:
    addr: int = _ITEM_TABLE_OFFSET + _ITEM_STRUCT_LEN * int(id_)
    data: tuple = struct.unpack_from(ITEM_STRUCT_FMT, rom, addr)
    item_data = GSTBSInternalItemData(
        id = id_, name = name, desc = desc, addr = addr,
        cost = data[0], item_type = data[1], flags = data[2], equip_compat = data[3],
        attack = data[6],
        defense = data[7],
        unleash_rate = data[8],
        use_type = data[9],
        unleash_id = data[11],
        use_effect = data[26],
        equip_effects = [[data[i], data[i+1]] for i in range(14, 25, 3)]
    )
    # individual description overrides can go here, i.e.
    # if (item_data.id == 171): desc = "Circlet: Use to delude enemies"
    return item_data


def load_item_data_table(rom: Rom, lines: dict[str, GSTBSInternalStringData]) -> dict[str, GSTBSInternalItemData]:
    item_data_table : dict[str, GSTBSInternalItemData] = dict()
    for i in range(_ITEM_TABLE_LEN):
        name = read_line(lines, str(_ITEM_NAME_OFFSET + i))
        if name == '?\x00': continue
        desc = read_line(lines, str(_ITEM_DESC_OFFSET + i))
        item_data_table[str(i)] = read_item(rom, i, name, desc)
    return item_data_table


def dump_item_data_table(data_table: dict[str, GSTBSInternalItemData], file_path: "Path") -> None:
    # these may require special handling per data type, so each table will have its own dump function
    temp_data = pickle.loads(pickle.dumps(data_table))  # faster than the deepcopy
    for k, v in temp_data.items():
        temp_data[k].name = format_line(v.name, 'pretty')
        temp_data[k].desc = format_line(v.desc, 'pretty')
    with open(file_path, 'w+b') as f:
        f.write(orjson.dumps(temp_data, option=orjson.OPT_INDENT_2))
        f.write(b'\n')


# def randomize_compatibilty():
#     pass
#
# def adjust_equip_prices():
#     pass
#
# def adjust_stats():
#     pass
#
# def shuffle_weapon_stats():
#     pass
#
# def shuffle_armor_stats():
#     pass
#
# def shuffle_weapon_effects():
#     pass
#
# def shuffle_armor_effects():
#     pass
#
# def shuffle_curses():
#     pass
#
# def disable_curses():
#     pass
#
# def sort_weapon_array():
#     pass
#
# def sort_armor_array():
#     pass
#
# def get_armor_score():
#     pass
