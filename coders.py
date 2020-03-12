from priority_queue import PriorityQueue
from tree import Tree
from codes import Code
from typing import Dict


def get_bytes(value: int, size: int):
    return value.to_bytes(size, byteorder="big")


def from_bytes(value: bytes):
    return int.from_bytes(value, byteorder="big")


class Encoder:
    def __init__(self, freq):
        self.freq = freq
        self.__codes: Dict[int, Code] = {}

    def generate_codes(self):
        queue = PriorityQueue()
        queue.create([(x["char"], x["num"]) for x in self.freq])

        while len(queue.col) > 1:
            left_elem = queue.get()
            right_elem = queue.get()

            node = Tree({"char": "null", "weight": left_elem[1] + right_elem[1]})
            if type(left_elem[0]) != Tree:
                node.add_left(Tree({"char": left_elem[0], "weight": left_elem[1]}))
            else:
                node.add_left(left_elem[0])

            if type(right_elem[0]) != Tree:
                node.add_right(Tree({"char": right_elem[0], "weight": right_elem[1]}))
            else:
                node.add_right(right_elem[0])

            queue.add(node, node.data["weight"])

        huffman_tree = queue.get()[0]
        self.__codes = huffman_tree.walk()

    def get_codes(self) -> Dict[int, Code]:
        return self.__codes

    def print_codes(self):
        for k, v in self.__codes.items():
            print("ch:", chr(k), "str_code:", v, "int_code", v.get_code())
