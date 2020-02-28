class Tree:
    def __init__(self, data: dict):
        self.left = None
        self.right = None
        self.data = data

    def add_right(self, r_tree):
        self.right = r_tree

    def add_left(self, l_tree):
        self.left = l_tree

    def walk(self, code: str = "", codes: dict = {}):
        if self.left:
            self.left.walk(code+"0")
        if self.right:
            self.right.walk(code+"1")
        if self.data["char"] != "null":
            codes[self.data["char"]] = code
        return codes
