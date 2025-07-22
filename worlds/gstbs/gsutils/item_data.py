# Ported from https://github.com/Karanum/gs2-randomiser2/blob/master/randomiser/game_data/items.js

import struct
import pickle
from dataclasses import dataclass
from typing import TYPE_CHECKING
import orjson

from .binary_utils import Rom, ITEM_STRUCT_FMT, ITEM_STRUCT_LEN
from .text_utils import read_line, format_line, GSTBSInternalStringData

if TYPE_CHECKING:
    from pathlib import Path

_ITEM_TABLE_OFFSET: int = 0x7B6A8
_ITEM_TABLE_LEN: int = 269
_ITEM_NAME_START: int = 386
_ITEM_DESC_START: int = 117


@dataclass
class GSTBSInternalItemData:
    id: int  # this is technically also an index. The dict key for each item will be str(id)
    name: str
    desc: str
    addr: int
    cost: int
    item_type: int
    flags: int
    equip_compat: int
    # icon: int  # NOTE is this an address? or an id?
    attack: int
    defense: int
    unleash_rate: int
    use_type: int
    unleash_id: int
    # attribute : int  # NOTE attribute might be able to be randomized later?
    use_effect: int  # moved up so that the equip effects array is last in the .json
    equip_effects: list[list[int]]


def read_item(rom: Rom, id_: int, name: str, desc: str) -> GSTBSInternalItemData:
    addr: int = _ITEM_TABLE_OFFSET + ITEM_STRUCT_LEN * int(id_)
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


def load_item_data(rom: Rom, lines: dict[str, GSTBSInternalStringData]) -> dict[str, GSTBSInternalItemData]:
    item_data: dict[str, GSTBSInternalItemData] = dict()
    for i in range(_ITEM_TABLE_LEN):
        name = read_line(lines, str(_ITEM_NAME_START + i))
        if name == '?\x00': continue
        desc = read_line(lines, str(_ITEM_DESC_START + i))
        item_data[str(i)] = read_item(rom, i, name, desc)
    return item_data


def dump_item_data(data: dict[str, GSTBSInternalItemData], file_path: "Path") -> None:
    # these may require special handling per data type, so each table will have its own dump function
    temp_data = pickle.loads(pickle.dumps(data))  # faster than the deepcopy method
    for k, v in temp_data.items():
        temp_data[k].name = format_line(v.name, 'pretty')
        temp_data[k].desc = format_line(v.desc, 'pretty')
    with open(file_path, 'w+b') as f:
        f.write(orjson.dumps(temp_data, option=orjson.OPT_INDENT_2))
        f.write(b'\n')
