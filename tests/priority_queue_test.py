from priority_queue import PriorityQueue


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




