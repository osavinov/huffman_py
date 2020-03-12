from typing import Dict, Optional
from codes import Code


class Tree:
    # instance attributes
    left: Optional["Tree"]
    right: Optional["Tree"]
    data: Dict

    # class attribute
    __codes: Dict[int, Code] = {}

    def __init__(self, data: Dict):
        self.left = None
        self.right = None
        self.data = data

    def add_right(self, r_tree: "Tree"):
        self.right = r_tree

    def add_left(self, l_tree: "Tree"):
        self.left = l_tree

    # code starts with leading 1
    def walk(self, code: int = 1) -> Dict[int, Code]:
        if self.left:
            new_code = code << 1
            new_code |= 0b0
            self.left.walk(new_code)
        if self.right:
            new_code = code << 1
            new_code |= 0b1
            self.right.walk(new_code)
        if self.data["char"] != "null":
            self.__codes[self.data["char"]] = Code(code)
        return self.__codes

    def clean(self):
        if self.left:
            self.left.clean()
        if self.right:
            self.right.clean()
        del self

    def check(self):
        node_weight: int = self.data.get("weight")
        if self.right is not None and self.left is not None:
            left_weight: int = self.left.data.get("weight")
            right_weight: int = self.right.data.get("weight")
            if left_weight + right_weight != node_weight:
                raise Exception("For node with weight %d doesn't match sum of children %d, %d" %
                                (node_weight, left_weight, right_weight))
