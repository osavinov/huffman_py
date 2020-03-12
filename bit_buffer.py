from codes import Code


class BitBuffer:
    __buf: int
    __new_buf: int  # if buf is full, we write rest of code into __new_buf
    __max_size: int

    def __init__(self, max_size: int):
        self.__buf = 1
        self.__new_buf = 1
        self.__max_size = max_size

    def __len__(self) -> int:
        return self.__buf.bit_length()-1

    # get str of 1, 0 bits excluding leading 1
    def __str__(self) -> str:
        return ("{0:%db}" % self.__len__()).format(self.__buf)[1:]

    # get code value excluding leading 1
    def value(self) -> int:
        return self.__buf & (2**self.__len__()-1)

    # get raw code value
    def get_buf(self) -> int:
        return self.__buf

    def __add_buf(self, c: Code):
        self.__buf <<= len(c)
        self.__buf |= c.value()

    def __add_new_buf(self, c: Code):
        self.__new_buf <<= len(c)
        self.__new_buf |= c.value()

    def is_full(self) -> bool:
        if self.__max_size - self.__len__() == 0:
            return True
        return False

    # returns true if buffer is full
    def add_code(self, c: Code) -> bool:
        rest = self.__max_size - self.__len__()
        if rest >= len(c):
            self.__add_buf(c)
            return False
        elif rest == 0:
            self.__add_new_buf(c)
            return True
        else:
            start, end = c.split(rest)  # end to the old buffer, start to the new one
            self.__add_buf(end)
            self.__add_new_buf(start)
            return True

    def swap(self):
        self.__buf = self.__new_buf
        self.__new_buf = 1
