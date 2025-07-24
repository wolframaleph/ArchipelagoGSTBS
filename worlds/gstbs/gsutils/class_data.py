from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pathlib import Path

_CLASS_DATA_OFFSET: int = 0


def read_class():
    raise NotImplementedError


def load_class_data():
    raise NotImplementedError


def dump_class_data():
    raise NotImplementedError
