import struct
import pickle
from dataclasses import dataclass
from typing import TYPE_CHECKING
import orjson

from .binary_utils import Rom, ABILITY_STRUCT_FMT, ABILITY_STRUCT_LEN
from .text_utils import read_line, format_line, GSTBSInternalStringData

if TYPE_CHECKING:
    from pathlib import Path

_DJINN_TABLE_OFFSET: int = 0


def read_djinni():
    raise NotImplementedError


def load_djinn_data():
    raise NotImplementedError


def dump_djinn_data():
    raise NotImplementedError
