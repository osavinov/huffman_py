from codes import Code


class BitBuffer:
    def __init__(self, max_size: int):
        self.__buf = 0
        self.__max_size = max_size

    def __len__(self) -> int:
        return self.__buf.bit_length()

    def __str__(self) -> str:
        return (("{0:%db}" % self.__len__()).format(self.get_code()))

    def add_code(self, c: Code) -> bool:
        rest = self.__max_size - self.__buf.bit_length()
        if rest >= len(c):
            self.__buf <<= len(c)
            self.__buf |= c.
            self.bit_buffer <<= (code.bit_length() - 1)
            self.bit_buffer |= code
        elif rest == 0:
            self.__write()
            self.bit_buffer <<= (code.bit_length() - 1)
            self.bit_buffer |= code
        else:
            self.bit_buffer <<= (rest - 1)
            self.bit_buffer |= self.__get_part(code, -rest)
            self.__write()
            self.bit_buffer <<= (rest - 1)
            self.bit_buffer |= self.__get_part(code, rest)