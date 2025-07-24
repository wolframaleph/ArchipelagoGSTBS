from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pathlib import Path

_ENEMY_DATA_OFFSET: int = 0


def read_enemy():
    raise NotImplementedError


def load_enemy_data():
    raise NotImplementedError


def dump_enemy_data():
    raise NotImplementedError
