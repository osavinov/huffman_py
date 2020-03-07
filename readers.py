import os
import binascii
from collections import defaultdict
from coders import from_bytes
from typing import List, Dict, Union, Any, Tuple


class ReadBuffer:
    def __init__(self, buffer_size: int = 1024*1024, filename: str = "text.txt"):
        self.buffer = None
        self.buffer_size = buffer_size
        self.filename = filename
        self.file = None
        self.freq = []
        self.portion = None
        self.filesize = 0

    def open(self):
        self.file = open(self.filename, "rb")
        self.filesize = os.stat(self.filename).st_size

    def read(self) -> bytes:
        self.portion = self.file.read(self.buffer_size)
        return self.portion

    def read_header(self) -> Tuple[Union[int, Any], Dict[str, str]]:
        file_size = from_bytes(self.file.read(4)) + 1
        codes_size = from_bytes(self.file.read(1))
        codes = dict()
        for i in range(codes_size):
            sym = from_bytes(self.file.read(1))
            size_code = from_bytes(self.file.read(1))
            code_int = int(binascii.hexlify(self.file.read(2)), 16)
            result_code = "{0:016b}".format(code_int)
            code = result_code[-size_code:]
            codes[code] = chr(sym)
            # print("Sym: ", sym, " code: ", code, " size_of_code: ", size_code, "result_code: ", result_code)
        return file_size, codes

    def convert_from_bytes(self) -> str:
        n = binascii.hexlify(self.portion)
        formatter = "{0:0%db}" % (len(self.portion)*8)
        return formatter.format((int(n, 16)))

    def scan_file(self) -> List[Dict[str, Union[int, Any]]]:
        self.file = open(self.filename, "rb")
        portion = self.read()
        freq = defaultdict(int)
        while portion:
            for c in portion:
                freq[c] += 1
            portion = self.read()
        self.file.close()
        self.freq = [{"char": k, "num": v} for k, v in freq.items()]
        return self.freq

    def close(self):
        self.file.close()
