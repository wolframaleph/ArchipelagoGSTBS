import sys
from pathlib import Path
# from os import SEEK_SET, SEEK_END

from .item_data import load_item_data_table, dump_item_data_table
from .text_utils import load_tree_data, load_string_table


file_dir_path = Path(__file__).resolve().parent

def main() -> None:
    with open(sys.argv[1], mode='rb') as rom_file:
        # rom_len: int = rom_file.seek(0, SEEK_END)  # get rom size
        # rom_file.seek(0, SEEK_SET)  # return cursor to beginning of file
        # out_rom: bytes = bytes(rom_len)
        # rom_file.readinto(out_rom)
        base_rom = rom_file.read()

    forest = load_tree_data(base_rom)
    lines = load_string_table(base_rom, forest)
    items = load_item_data_table(base_rom, lines)
    dump_item_data_table(items, file_dir_path / 'items.json')


if __name__ == '__main__':
    main()