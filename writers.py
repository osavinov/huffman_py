from coders import get_bytes


class BytesBufferWriter:
    def __init__(self, buffer_size: int = 1024*128, filename: str = "result.huf"):
        # bit-storage for code-string, binary codes 'concatenates', leading 1 uses for bit_length()
        self.bit_buffer: int = 1
        # bytes-buffer ready for writing
        self.bytes_buffer: bytes = b''
        # maximum size of bytes_buffer, buffer_size * 8 must be equal with bit_buffer.bit_length()
        self.buffer_size: int = buffer_size
        # binary file we want to write
        self.file = open(filename, "wb")

    def __write(self):
        self.bytes_buffer = int.to_bytes(self.bit_buffer, self.buffer_size, byteorder="big")
        self.__write_to_file()
        self.bytes_buffer = b''
        self.bit_buffer = 0

    def __write_to_file(self):
        self.file.write(self.bytes_buffer)

    def close(self):
        size_bits = len(self.bytes_buffer) * 8
        if size_bits > 0:
            rest = size_bits % 8
            size_bytes = size_bits // 8
            if rest > 0:
                self.bytes_buffer = get_bytes(int(self.string_buffer[:-rest], 2), size_bytes)
                self.__write_to_file()
                last_byte = self.string_buffer[-rest:] + "0"*(8-rest)
                self.bytes_buffer = get_bytes(int(last_byte, 2), 1)
                self.__write_to_file()
            else:
                self.bytes_buffer = get_bytes(int(self.string_buffer, 2), size_bytes)
                self.__write_to_file()
        self.file.close()

    def write_header(self, filesize: int, codes: dict):
        size_b = get_bytes(filesize, 4)
        self.file.write(size_b)
        codes_size = len(codes) - 1
        self.file.write(get_bytes(codes_size, 1))
        for sym, code in codes.items():
            self.file.write(get_bytes(sym, 1))
            size = len(code)
            self.file.write(get_bytes(size, 1))
            result_code = "0" * (16-size) + code
            self.file.write(get_bytes(int(result_code, 2), 2))
            # print("Sym: ", sym, " code: ", code, " size_of_code: ", size, "result_code: ", result_code)


class WriteBuffer:
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
