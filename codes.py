class Code:
    __code: int

    # we initialize with value with leading 1, because codes might start with 0
    def __init__(self, val: int):
        self.__code = 0
        self.__code >>= val.bit_length()
        self.__code |= val

    def __len__(self) -> int:
        return self.__code.bit_length()-1

    def __getitem__(self, ind) -> int:
        return self.__code & (2**ind)

    # get str of 1, 0 bits excluding leading 1
    def __str__(self) -> str:
        return (("{0:%db}" % self.__len__()).format(self.__code)).lstrip()[1:]

    # get code value excluding leading 1
    def value(self) -> int:
        return self.__code & (2**(self.__code.bit_length()-1)-1)

    # get raw code value
    def get_code(self) -> int:
        return self.__code

    def get_part(self, num: int) -> int:
        if num == 0:
            return 0
        elif num < 0:
            return self.value() >> (self.__len__()+num)
        elif num > 0:
            return self.value() & (2**num - 1)
