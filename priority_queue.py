from typing import List, TypeVar, Generic, Tuple

T = TypeVar("T")


class PriorityQueue(Generic[T]):
    col: List[Tuple[T, int]]

    def __init__(self):
        self.col = []

    def create(self, seq: List):
        self.col = seq
        self.col.sort(key=lambda t: t[1])

    def add(self, elem: T, priority: int):
        self.col.append((elem, priority))
        self.col.sort(key=lambda t: t[1])

    def get(self) -> T:
        if len(self.col) == 0:
            return None
        elem = self.col[0]
        del self.col[0]
        return elem

    def is_empty(self) -> bool:
        if len(self.col) == 0:
            return True
        else:
            return False

    def clean(self):
        self.col.clear()

    def print(self):
        print(self.col)

    def get_content(self) -> List[Tuple[T, int]]:
        return self.col
