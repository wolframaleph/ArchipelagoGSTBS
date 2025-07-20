import struct
import re
import math
from dataclasses import dataclass
import orjson

from .binary_utils import gbarom_bitmask, enforce_c_type_range, BitReader
from .gshuffman import GSHuffmanForest, GSHuffmanTree, Node

_HUFFMAN_OFFSET: int = 0x3842c
_STRINGS_OFFSET: int = 0x736b8
_NUM_STRINGS: int = 10722

_NON_PRINTABLES_REGEX = re.compile('[^ -~]')  # [^a-zA-Z0-9?:;,\\&\\'\\-\\(\\) ]


@dataclass
class StringPtrs:
    data_ptr: int  # uint32_t
    lengths_ptr: int  # uint32_t
    def __init__(self, data_ptr: int, lengths_ptr: int) -> None:
        self.data_ptr = gbarom_bitmask(data_ptr)
        self.lengths_ptr = gbarom_bitmask(lengths_ptr)


@dataclass
class HuffmanPtrs:
    forest_ptr: int  # uint32_t
    offsets_ptr: int  # uint32_t
    def __init__(self, data_ptr: int, offsets_ptr: int):
        self.forest_ptr = gbarom_bitmask(data_ptr)
        self.offsets_ptr = gbarom_bitmask(offsets_ptr)


@dataclass
class GSTBSInternalStringData:
    id: str
    addr: int
    text: str


def load_string_table(rom, forest) -> dict[str, GSTBSInternalStringData]:
    string_id: int = 0
    i: int = 0
    corpus: dict[str, GSTBSInternalStringData] = dict()
    while string_id < _NUM_STRINGS:
        string_ptrs: StringPtrs = StringPtrs(*struct.unpack_from(f'<II', rom, _STRINGS_OFFSET + i * 8))  # 2 pointers
        line_data_ptr: int = string_ptrs.data_ptr
        j: int = 0
        while j < 256 and string_id < _NUM_STRINGS:
            corpus[str(string_id)] = decompress_string(rom, forest, line_data_ptr, str(string_id))
            len_bytes, = struct.unpack_from(f'<B', rom, string_ptrs.lengths_ptr + j) # size is only 1 byte
            if len_bytes == 255: raise(RuntimeError('Too many bytes'))  # NOTE needs better error message
            line_data_ptr += len_bytes
            j+=1; string_id +=1
        i += 1
    return corpus


def dump_string_table(data_table, file_path) -> None:
    # these may require special handling per data type, so each table will have its own dump function
    with open(file_path, 'w+b') as f:
        f.write(orjson.dumps(data_table, option=orjson.OPT_INDENT_2))
        f.write(b'\n')


def load_tree_data(rom) -> GSHuffmanForest:
    forest: GSHuffmanForest = GSHuffmanForest()
    huffman_ptrs: HuffmanPtrs = HuffmanPtrs(*struct.unpack_from(f'<II', rom, _HUFFMAN_OFFSET))
    tree_offset_ptr: int = huffman_ptrs.offsets_ptr
    for tree_symbol in range(256):
        tree_offset, = struct.unpack_from(f'<H', rom, tree_offset_ptr)
        tree_addr = huffman_ptrs.forest_ptr + tree_offset
        stack = list()

        node = Node()  # create root for the current symbol's Huffman tree
        forest[tree_symbol] = GSHuffmanTree(node)  # initalize tree with root node
        stack.append(node)  # places shared reference to root node on stack

        offset: float = .5  # moves the the address back by 3 bytes every other 0b1, starting with the first
        shift: int = 0  # addresses the correct 12 bits of the 24 bit (3 byte) read

        bit_reader = BitReader(rom, tree_addr)
        for _ in range(512):  # reads the next block of 512 bits (64 bytes)
            node = stack.pop()
            if next(bit_reader) == 1:
                offset += 0.5
                shift += 12
                char_addr = tree_addr - 3 * math.floor(offset)
                # the chars are organized into groups of 12 bits, so only retrieve 3 bytes and use shift
                # while using gbarom_bitmask() and '<I' would have worked here, it is a misuse of the function
                char = int.from_bytes(struct.unpack_from(f'<BBB', rom, char_addr), byteorder='little', signed=False)
                char >>= (shift % 24)
                masked_char = char & 0xFFF
                node.symbol = masked_char
            else:
                node.left = Node()
                node.right = Node()
                stack.extend([node.right, node.left])  # using append would add a list of 2 nodes to the stack instead
            if len(stack) == 0: break
        tree_offset_ptr += 2
    return forest


def decompress_string(rom, forest: GSHuffmanForest, text_ptr, id_: str):
    bit_reader = BitReader(rom, text_ptr)
    text: str = ''
    char: int = 0
    while True:  # emulate c do-while loop
        node: Node = forest[char].root
        while node.symbol is None:  # 0 should be considered truthy in this context
            if next(bit_reader) == 1:
                node = node.right
            else:
                node = node.left
        char = enforce_c_type_range('uchar', node.symbol)
        text += chr(char)
        if not char: break
    return GSTBSInternalStringData(id_, text_ptr, text)


def read_line(lines, id_):
    return lines[id_].text


def format_line(s: str, style: str = None):
    match style:
        case 'pretty': return _NON_PRINTABLES_REGEX.sub('', s).strip()
        case 'brackets': return _NON_PRINTABLES_REGEX.sub(lambda x: f'[{ord(x.group())}]', s)
        case 'utf8': return s
        case _: return s
