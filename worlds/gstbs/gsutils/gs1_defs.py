import struct
from dataclasses import dataclass

# GENERAL NOTE unknown bytes will be read but not stored for the sake of consistent indexing

@dataclass
class GSTBSInternalStringData:
    id: str
    addr: int
    text: str

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
ITEM_STRUCT_LEN: int = 44
if struct.calcsize(ITEM_STRUCT_FMT) != ITEM_STRUCT_LEN:
    raise RuntimeError(f'{ITEM_STRUCT_FMT} size is incorrect')
item_struct = struct.Struct(ITEM_STRUCT_FMT)

@dataclass
class GSTBSInternalItemData:
    id: int  # this is technically also an index. The dict key for each item will be str(id)
    name: str
    desc: str
    addr: int
    cost: int
    item_type: int
    flags: int
    equip_compat: int
    # icon: int  # NOTE is this an address? or an id?
    attack: int
    defense: int
    unleash_rate: int
    use_type: int
    unleash_id: int
    # attribute : int  # NOTE attribute might be able to be randomized later?
    use_effect: int  # moved up so that the equip effects array is last in the .json
    equip_effects: list[list[int]]


# ability struct definition
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
ABILITY_STRUCT_LEN: int = 16
if struct.calcsize(ABILITY_STRUCT_FMT) != ABILITY_STRUCT_LEN:
    raise RuntimeError(f'{ABILITY_STRUCT_FMT} size is incorrect')
ability_struct = struct.Struct(ABILITY_STRUCT_FMT)

@dataclass
class GSTBSInternalAbilityData:
    id: int  # this is technically also an index. The dict key for each item will be str(id)
    name: str
    desc: str
    addr: int
    type: str
    target: int
    damage_type: int
    element: int
    range: int
    cost: int
    power: int
    effect: int
