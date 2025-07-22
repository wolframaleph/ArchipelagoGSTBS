import struct
import pickle
from dataclasses import dataclass
from typing import TYPE_CHECKING
import orjson

from .binary_utils import Rom, ABILITY_STRUCT_FMT, ABILITY_STRUCT_LEN
from .text_utils import read_line, format_line, GSTBSInternalStringData

if TYPE_CHECKING:
    from pathlib import Path

_SUMMON_DATA_OFFSET = 0

# const summons = ["Venus", "Mercury", "Mars", "Jupiter", "Ramses", "Nereid", "Kirin", "Atalanta",
#     "Cybele", "Neptune", "Tiamat", "Procne", "Judgment", "Boreas", "Meteor", "Thor"]


def load_summon_data():
    pass


def dump_summon_data():
    pass
