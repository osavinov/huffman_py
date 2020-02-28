import os
import binascii
from collections import defaultdict


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

    def read(self):
        self.portion = self.file.read(self.buffer_size)
        return self.portion

    def read_sourcefile_size(self):
        size_b = self.file.read(4)
        size = int.from_bytes(size_b, byteorder="big")
        return size

    def convert_from_bytes(self):
        n = binascii.hexlify(self.portion)
        frmt = "{0:0%db}" % (len(self.portion)*8)
        return frmt.format((int(n, 16)))

    def scan_file(self):
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
