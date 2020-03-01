class BytesBufferWriter:
    def __init__(self, buffer_size: int = 1024*128, filename: str = "result.huf"):
        self.string_buffer = ""
        self.bytes_buffer = None
        self.buffer_size = buffer_size
        self.file = open(filename, "wb")

    def add(self, code):
        rest = self.buffer_size * 8 - len(self.string_buffer)

        if rest >= len(code):
            self.string_buffer += code
        elif rest == 0:
            self.__convert_to_bytes()
            self.string_buffer += code
        else:
            self.string_buffer += code[:rest]
            self.__convert_to_bytes()
            self.string_buffer += code[rest:]

    def __convert_to_bytes(self):
        self.bytes_buffer = int(self.string_buffer, 2).to_bytes(self.buffer_size, byteorder="big")
        self.__write_to_file()
        self.string_buffer = ""
        self.bytes_buffer = None

    def __write_to_file(self):
        self.file.write(self.bytes_buffer)

    def close(self):
        size_bits = len(self.string_buffer)
        if size_bits > 0:
            rest = size_bits % 8
            size_bytes = size_bits // 8
            if rest > 0:
                self.bytes_buffer = int(self.string_buffer[:-rest], 2).to_bytes(size_bytes, byteorder="big")
                self.__write_to_file()
                last_byte = self.string_buffer[-rest:] + "0"*(8-rest)
                self.bytes_buffer = int(last_byte, 2).to_bytes(1, byteorder="big")
                self.__write_to_file()
            else:
                self.bytes_buffer = int(self.string_buffer, 2).to_bytes(size_bytes, byteorder="big")
                self.__write_to_file()
        self.file.close()

    def __write_bytes(self, value: int, size: int):
        self.file.write(value.to_bytes(size, byteorder="big"))

    def write_header(self, filesize: int, codes: dict):
        size_b = filesize.to_bytes(4, byteorder="big")
        self.file.write(size_b)
        codes_size = len(codes)
        print("Codes table size: ", codes_size)
        self.file.write(codes_size.to_bytes(1, byteorder="big"))
        for sym, code in codes.items():
            self.file.write(sym.to_bytes(1, byteorder="big"))
            size = len(code)
            self.file.write(size.to_bytes(1, byteorder="big"))
            result_code = "0" * (16-size) + code
            self.file.write(int(result_code, 2).to_bytes(2, byteorder="big"))
            print("Sym: ", sym, " code: ", code, " size_of_code: ", size, "result_code: ", result_code)


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
