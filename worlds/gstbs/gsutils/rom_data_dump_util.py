import sys
from pathlib import Path

from .item_data import load_item_data, dump_item_data
from .ability_data import load_ability_data, dump_ability_data
from .text_utils import load_tree_data, load_string_table


file_dir_path = Path(__file__).resolve().parent / 'out'

def main() -> None:
    with open(sys.argv[1], mode='rb') as rom_file:
        base_rom = rom_file.read()

    forest = load_tree_data(base_rom)
    lines = load_string_table(base_rom, forest)
    items = load_item_data(base_rom, lines)
    abilities = load_ability_data(base_rom, lines)

    dump_item_data(items, file_dir_path / 'items.json')
    dump_ability_data(abilities, file_dir_path / 'abilities.json')


if __name__ == '__main__':
    main()