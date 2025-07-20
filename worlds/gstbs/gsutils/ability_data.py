# Ported from https://github.com/Karanum/gs2-randomiser2/blob/master/randomiser/game_data/abilities.js

import struct
import pickle
from dataclasses import dataclass
from typing import TYPE_CHECKING
import orjson

from .binary_utils import Rom, ABILITY_STRUCT_FMT, ABILITY_STRUCT_LEN
from .text_utils import read_line, format_line, GSTBSInternalStringData

if TYPE_CHECKING:
    from pathlib import Path

_ABILITY_TABLE_OFFSET: int = 0x7EE58
_ABILITY_TABLE_LEN: int = 519
_ABILITY_NAME_START: int = 819
_ABILITY_DESC_START: int = 1338


@dataclass
class GSTBSInternalAbilityData:
    id: int  # this is technically also an index. The dict key for each item will be str(id)
    name: str
    desc: str
    addr: int
    type: str
    target: int
    damage_type: int
    element: int
    range: int
    cost: int
    power: int
    effect: int


def get_ability_type(id_: int) -> str:
    if id_ < 3: return 'n/a'
    elif id_ < 210: return 'Psynergy'
    elif id_ < 250: return 'Unleash'
    elif id_ < 300: return 'Item'
    elif id_ < 380: return 'Djinn'
    elif id_ < 420: return 'Summon'
    elif id_ < _ABILITY_TABLE_LEN: return 'Enemy'
    else: raise ValueError(f'id {id_} exceeds length of ability table')


def read_ability(rom: Rom, id_: int, name: str, desc: str): # -> GSTBSInternalAbilityData:
    addr: int = _ABILITY_TABLE_OFFSET + ABILITY_STRUCT_LEN * int(id_)
    data: tuple = struct.unpack_from(ABILITY_STRUCT_FMT, rom, addr)
    ability_data = GSTBSInternalAbilityData(
        id = id_,
        name = name,
        desc = desc,
        addr = addr,
        type = get_ability_type(id_),
        # usability = 0,
        target = data[0],
        damage_type = data[1] & 0x0F,  # this assumes the data is formatted the same as in TLA
        element = data[2],
        range = data[7],
        cost = data[8],
        power = data[9],
        effect = data[3]
    )
    return ability_data


def load_ability_data(rom: Rom, lines: dict[str, GSTBSInternalStringData]) -> dict[str, GSTBSInternalAbilityData]:
    ability_data: dict[str, GSTBSInternalAbilityData] = dict()
    for i in range(_ABILITY_TABLE_LEN):
        name = read_line(lines, str(_ABILITY_NAME_START + i))
        if name == '?\x00': continue
        if name == '=\x00': continue
        desc = read_line(lines, str(_ABILITY_DESC_START + i))
        ability_data[str(i)] = read_ability(rom, i, name, desc)
    return ability_data


def dump_ability_data(data: dict[str, GSTBSInternalAbilityData], file_path: 'Path') -> None:
    # these may require special handling per data type, so each table will have its own dump function
    temp_data = pickle.loads(pickle.dumps(data))
    for k, v in temp_data.items():
        temp_data[k].name = format_line(v.name, 'pretty')
        temp_data[k].desc = format_line(v.desc, 'pretty')
    with open(file_path, 'w+b') as f:
        f.write(orjson.dumps(temp_data, option=orjson.OPT_INDENT_2))
        f.write(b'\n')

# def write_to_rom():
#     pass
#
# def get_ability_element():
#     pass
#
# def setStartingPsynergy():
#     pass
#
# def adjust_ability_power():
#     pass
#
# def adjust_psynergy_cost():
#     pass
#
# def randomise_ability_range():
#     pass
