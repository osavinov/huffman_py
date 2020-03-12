from typing import Dict, List

from coders import get_bytes
from bit_buffer import BitBuffer
from codes import Code


class BytesBufferWriter:
    bit_buffer: BitBuffer
    bytes_buffer: bytes
    buffer_size: int

    def __init__(self, buffer_size: int = 1024*128, filename: str = "result.huf"):
        # bit-storage for code-string, binary codes 'concatenates', leading 1 uses for bit_length()
        self.bit_buffer: BitBuffer = BitBuffer(buffer_size)

        # bytes-buffer ready for writing
        self.bytes_buffer: bytes = b''

        # maximum size of bytes_buffer, buffer_size * 8 must be equal with bit_buffer.bit_length()
        self.buffer_size: int = buffer_size

        # binary file we want to write
        self.file = open(filename, "wb")

    # converts bit_buffer to bytes_buffer, writes it to file, splash bytes_buffer
    def __write(self):
        self.bytes_buffer = int.to_bytes(self.bit_buffer.value(), self.buffer_size, byteorder="big")
        self.__write_to_file()
        self.bytes_buffer = b''

    def __write_to_file(self):
        self.file.write(self.bytes_buffer)

    def add_code(self, c: Code):
        if self.bit_buffer.add_code(c):
            self.__write()
            self.bit_buffer.swap()

    def close(self):
        if self.bit_buffer.is_full():
            self.__write()
        else:
            self.bytes_buffer = int.to_bytes(self.bit_buffer.value(), len(self.bit_buffer) // 8 + 1, byteorder="big")
            self.__write_to_file()
            self.bytes_buffer = b''
        self.file.close()

    # size of source file (4 bytes)
    # size codes table (1 byte)
    # symbol (1 byte), size of code (1 byte), code (2 bytes) = tuple in 4 bytes, maximum = 256 * 4 = 1024 bytes
    def write_header(self, filesize: int, codes: Dict[int, Code]):
        size_b = get_bytes(filesize, 4)
        self.file.write(size_b)
        codes_size = len(codes) - 1
        self.file.write(get_bytes(codes_size, 1))
        for sym, code in codes.items():
            self.file.write(get_bytes(sym, 1))
            size = len(code)
            self.file.write(get_bytes(size, 1))
            self.file.write(get_bytes(code.value(), 2))
            print("Sym: ", chr(sym), " code: ", code, " size_of_code: ", size, "code: ", code)


class WriteBuffer:
    bytes_buffer: List[int]
    buffer_size: int

    def __init__(self, buffer_size: int = 1024*1024, filename: str = "source.dat"):
        self.bytes_buffer = []
        self.buffer_size = buffer_size
        self.file = open(filename, "wb")

    def add(self, code):
        if self.bytes_buffer and len(self.bytes_buffer) == self.buffer_size:
            self.__write_to_file()
        self.bytes_buffer.append(ord(code))

    def __write_to_file(self):
        self.file.write(bytes(self.bytes_buffer))
        self.string_buffer = []

    def close(self):
        self.__write_to_file()
        self.file.close()
