class PriorityQueue:
    def __init__(self):
        self.col = []

    def create(self, l):
        self.col = l
        self.col.sort(key=lambda t: t[1])

    def add(self, elem, priority):
        self.col.append((elem, priority))
        self.col.sort(key=lambda t: t[1])

    def get(self):
        if len(self.col) == 0:
            return None
        elem = self.col[0]
        del self.col[0]
        return elem

    def is_empty(self):
        if len(self.col) == 0:
            return True
        else:
            return False

    def print(self):
        print(self.col)


def main():
    pq = PriorityQueue()
    pq.add("a", 13)
    pq.print()
    pq.add("b", 14)
    pq.print()
    pq.add("c", 2)
    pq.print()
    pq.add("d", 4)
    pq.print()
    pq.add("e", 1)
    pq.print()

    elem1 = pq.get()
    elem2 = pq.get()
    pq.print()
    pq.add(None, elem1[1]+elem2[1])
    pq.print()


if __name__ == "__main__":
    main()
