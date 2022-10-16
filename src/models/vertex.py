import typing as t


class Vertex(t.NamedTuple):
    number: int
    x: float
    y: float

    def __repr__(self) -> str:
        return str(self.number)
