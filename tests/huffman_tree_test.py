from tree import Tree


class TestHuffmanTree:
    tree: Tree

    def setup(self):
        self.tree = Tree({"char": "null", "weight": 15})

    def test_tree_get_nodes_code(self):
        self.tree.add_left(Tree({"char": "l", "weight": 5}))
        self.tree.add_right(Tree({"char": "r", "weight": 10}))
        codes_table = self.tree.walk()
        left_code = codes_table.get(ord("l"))
        right_code = codes_table.get(ord("r"))
        self.tree.check()
        assert left_code.value() == 0
        assert right_code.value() == 1
        assert str(left_code) == "0", "Test failed! Actual left_code: '%s'" % left_code
        assert str(right_code) == "1", "Test failed! Actual right_code: '%s'" % right_code
        self.tree.clean()
