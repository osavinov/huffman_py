from priority_queue import PriorityQueue
from tree import Tree
from coders import Encoder

from typing import List, Dict, Any


class TestPriorityQueue:
    pq: PriorityQueue

    def setup(self):
        self.pq = PriorityQueue()

    def test_add_to_queue(self):
        self.pq.add("a", 13)
        content: list = self.pq.get_content()
        assert ("a", 13) in content, "Test failed! Add doesn't work"

    def test_add_and_get_from_queue(self):
        self.pq.add("b", 14)
        elem = self.pq.get()
        assert elem == ("b", 14), "Test failed! Get doesn't work"

    def test_create_queue(self):
        seq = [("a", 1), ("b", 2), ("c", 3)]
        self.pq.create(seq)
        content: list = self.pq.get_content()
        assert seq == content, "Test failed! Create doesn't work"

    def test_check_queue_sort(self):
        self.pq.add("a", 12)
        self.pq.add("b", 2)
        self.pq.add("c", 3)
        content: list = self.pq.get_content()
        assert [("b", 2), ("c", 3), ("a", 12)] == content, "Test failed! Sort doesn't work"


class TestHuffmanTree:
    def test_tree_get_nodes_code(self):
        tree = Tree({"char": "null", "weight": 15})
        tree.add_left(Tree({"char": "l", "weight": 5}))
        tree.add_right(Tree({"char": "r", "weight": 10}))
        codes = tree.walk()
        left_code = codes.get("l")
        right_code = codes.get("r")
        tree.check()
        assert left_code.value() == 0
        assert right_code.value() == 1
        assert str(left_code) == "0", "Test failed! Actual left_code: '%s'" % left_code
        assert str(right_code) == "1", "Test failed! Actual right_code: '%s'" % right_code
        tree.clean()


class TestEncoder:
    def test_encoder_get_codes(self):
        freq: List[Dict[str, Any]] = [{"char": "A", "num": 1}, {"char": "B", "num": 4}, {"char": "C", "num": 2}]
        encoder = Encoder(freq)
        encoder.generate_codes()
        codes = encoder.get_codes()
        a_code = codes.get("A")
        b_code = codes.get("B")
        c_code = codes.get("C")
        assert str(a_code) == "00"
        assert str(b_code) == "1"
        assert str(c_code) == "01"

