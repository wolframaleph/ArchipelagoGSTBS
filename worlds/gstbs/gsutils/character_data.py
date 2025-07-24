from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pathlib import Path

_CHARACTER_STATS_OFFSET: int = 0


def read_stats():
    raise NotImplementedError


def load_character_data():
    raise NotImplementedError


def dump_character_data():
    raise NotImplementedError
