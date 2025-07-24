from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pathlib import Path

_DJINN_TABLE_OFFSET: int = 0


def read_djinni():
    raise NotImplementedError


def load_djinn_data():
    raise NotImplementedError


def dump_djinn_data():
    raise NotImplementedError
