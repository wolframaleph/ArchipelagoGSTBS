import sys
import struct
import enum
from os import SEEK_SET, SEEK_END
from typing import Union, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def gbarom_bitmask(val) -> int:
    return val & 0x00ffffff  # ROM data is addressed starting at 0x08000000 on the GBA


class BufferMode(enum.Enum):
    READONLY = 0,
    READWRITE = 1


class Rom:
    buffer: bytes | bytearray
    mem_view: memoryview
    def __init__(self, filename: Union[str, "Path"],  mode: BufferMode = BufferMode.READONLY):
        if mode == BufferMode.READONLY:
            with open(filename, mode='rb') as f:
                self.buffer : bytes = f.read()
        elif mode ==  BufferMode.READWRITE:
            with open(filename, mode='rb') as f:
                rom_len: int = f.seek(0, SEEK_END)  # get rom size
                f.seek(0, SEEK_SET)  # return cursor to beginning of file
                self.buffer: bytearray = bytearray(rom_len)
                f.readinto(self.buffer)
        else:
            raise RuntimeError
        self.mem_view = memoryview(self.buffer)

    def read_bytes(self, addr, length):
        start_addr = gbarom_bitmask(addr)
        end_addr = start_addr + length
        return self.mem_view[start_addr:end_addr]

    def write_bytes(self, addr, data):
        start_addr = gbarom_bitmask(addr)
        end_addr = start_addr + len(data)
        self.mem_view[start_addr:end_addr] = data

    def iter_bits(self, addr):
        byte_addr = gbarom_bitmask(addr)
        while True:
            bits = self.mem_view[addr]
            for _ in range(8):
                yield bits & 1
                bits >>= 1
            addr += 1

    def iter_bits_bounded(self, addr, len_bytes):
        start_addr = gbarom_bitmask(addr)
        end_addr = start_addr + len_bytes
        for byte in self.mem_view[start_addr:end_addr]:
            for _ in range(8):
                yield byte & 1
                byte >>= 1


class BitReader:
    # adapted from tarpman's https://github.com/gsret/goldensun/blob/master/tools/unpack_strings.c
    def __init__(self, rom: Rom, ptr):
        self.rom : Rom = rom
        self.ptr : int = ptr  # uint8_t *, so uint32_t
        self.bits : int = 0  # uint8_t
        self.avail : int = 0  # uint8_t

    def __next__(self) -> int:
        if self.avail == 0:
            self.bits, = struct.unpack_from('<B', self.rom.mem_view, self.ptr)
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
