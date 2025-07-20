import struct
from typing import Optional

# Create union of binary data types
type Rom = bytes | bytearray | memoryview


class BitReader:
    # adapted from tarpman's https://github.com/gsret/goldensun/blob/master/tools/unpack_strings.c
    def __init__(self, rom: Rom, ptr):
        self.rom : Rom = rom
        self.ptr : int = ptr  # uint8_t *, so uint32_t
        self.bits : int = 0  # uint8_t
        self.avail : int = 0  # uint8_t

    def __next__(self) -> int:
        if self.avail == 0:
            self.bits, = struct.unpack_from('<B', self.rom, self.ptr)
            self.ptr += 1  # move to next byte address
            self.avail = 8
        bit = self.bits & 1
        self.bits >>= 1
        self.avail -= 1
        return bit

    def __str__(self) -> str:
        return f'Addr: {self.ptr:#010x}, Bits: {self.bits:#010b}, Available: {self.avail}'


class OutOfCTypeRangeError(ValueError):
    default_message: str = 'is outside of C standards for type'
    def __init__(self, type_: str, value: int, message: Optional[str] = None):
        self.type : str = type_
        self.value : int = value
        self.message : str = message if message is not None else OutOfCTypeRangeError.default_message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.value} {self.message} {self.type}'


def enforce_c_type_range(type_, value) -> int:
    match type_:
        case 'uchar':
            if not (0 <= value <= 255): raise OutOfCTypeRangeError(type_, value)
        case 'ubyte':
            if not (0 <= value <= 255): raise OutOfCTypeRangeError(type_, value)
    return value


def gbarom_bitmask(val) -> int:
    return val & 0x00ffffff  # ROM data is addressed starting at 0x08000000 on the GBA


# NOTE unknown bytes will be read but not stored for the sake of consistent indexing

# item struct definition
# NOTE credit to the GSTLA info docs - (Should determine proper attribution)
# 00 SHORT = Price
# 02 BYTE = Item type
# 03 BYTE = Flags
#   01 = Curses when equipped.
#   02 = Can’t be removed.
#   04 = A rare item. (If dropped, can be bought back from shops.)
#   08 = An important item. (Can’t be dropped.)
#   10 = Carry up to 30.
#   20 = Transfer-denied. (Items cannot be transferred from GS1 to GS2.)
#   40 = Unused
#   80 = Unused
# 04 BYTE = Equippable by flags
# 05 BYTE = ?
# 06 SHORT = Icon
# 08 SHORT = Attack
# 0a BYTE = Defense
# 0b BYTE = Unleash rate
# 0c BYTE = Use type
# 0d BYTE = ?
# 0e SHORT = Unleash ability
# 10 WORD = ?
# 14 WORD = Attribute (Earth, Water, Fire, Wind, None)
# 18 Equipped effects: (x4)
#   BYTE = Effect while equipped
#   BYTE = Value
#   SHORT = May or may not be unused/part of above value.
# 28 SHORT = Use ability
# 2a SHORT = ?
ITEM_STRUCT_FMT: str = f'<HBBBBHhbBBBHII{4*"BbH"}HH'

# 0807EE58 = Ability data (16 bytes per entry)
# 00 BYTE - Target
# 01 BYTE - Type of move + Can be used in / outside of battle
# 02 BYTE - Element
# 03 BYTE - Ability Effect
# 04 SHORT - Icon (might be a BYTE joined with a second unused one; have not checked if GS1 uses both bytes for this)
# 06 BYTE - ???
# 07 BYTE - ???
# 08 BYTE - Range
# 09 BYTE - PP Cost
# 0a SHORT - Power
# oc BYTE - Utility to use
# 0d BYTE - ???
# 0e BYTE - ???
# 0f BYTE - ???
ABILITY_STRUCT_FMT: str = '<BBBBHBBBBHBBBB'
# TODO add guards