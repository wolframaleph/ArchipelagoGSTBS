import sys
import time
from pathlib import Path

from .item_data import load_item_data, dump_item_data
from .ability_data import load_ability_data, dump_ability_data
from .text_utils import load_tree_data, load_string_table
from .rom_utils import Rom, BufferMode

file_dir_path = Path(__file__).resolve().parent / 'out'

def main() -> None:
    base_rom = Rom(sys.argv[1], BufferMode.READONLY)
    forest = load_tree_data(base_rom)
    lines = load_string_table(base_rom, forest)
    items = load_item_data(base_rom, lines)
    abilities = load_ability_data(base_rom, lines)

    dump_item_data(items, file_dir_path / 'items.json')
    dump_ability_data(abilities, file_dir_path / 'abilities.json')


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f'\nInternal execution took {time.time() - start_time} seconds')