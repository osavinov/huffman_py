from typing import List, Dict, Any
from coders import Encoder
from codes import Code
from bit_buffer import BitBuffer


class TestEncoderAndBitBuffer:
    freq: List[Dict[str, Any]]
    encoder: Encoder
    codes: Dict[int, Code]

    def setup(self):
        self.freq = [{"char": "A", "num": 1}, {"char": "B", "num": 4}, {"char": "C", "num": 2}]
        self.encoder = Encoder(self.freq)
        self.encoder.generate_codes()
        self.codes = self.encoder.get_codes()

    def test_split_code(self):
        c: Code = Code(0b1110101)
        start, end = c.split(3)
        assert start.get_code() == 0b1101
        assert end.get_code() == 0b1110

    def test_encoder_get_codes(self):
        codes: Dict[int, Code] = self.encoder.get_codes()
        a_code = codes.get(ord("A"))
        b_code = codes.get(ord("B"))
        c_code = codes.get(ord("C"))
        assert str(a_code) == "00"
        assert str(b_code) == "1"
        assert str(c_code) == "01"

    def test_bitbuffer_add_codes(self):
        input_str: str = "ABBCBBC"
        bit_buffer: BitBuffer = BitBuffer(256)
        for c in input_str.encode():
            bit_buffer.add_code(self.codes.get(c))
        assert bit_buffer.value() == 221
        assert str(bit_buffer) == "0011011101"

    def test_bitbuffer_full(self):
        input_str: str = "CCCCCC"
        bit_buffer: BitBuffer = BitBuffer(8)
        for c in input_str.encode():
            if bit_buffer.add_code(self.codes.get(c)):
                assert bit_buffer.value() == 85  # 0b01010101
                assert str(bit_buffer) == "01010101"
                bit_buffer.swap()
        assert bit_buffer.value() == 5
        assert str(bit_buffer) == "0101"

    def test_bitbuffer_overflow_on_border(self):
        input_str: str = "CCC"  # 010101
        bit_buffer: BitBuffer = BitBuffer(5)
        for c in input_str.encode():
            if bit_buffer.add_code(self.codes.get(c)):
                assert bit_buffer.value() == 10  # 01010
                assert str(bit_buffer) == "01010"
                bit_buffer.swap()
        assert bit_buffer.value() == 1
        assert str(bit_buffer) == "1"
