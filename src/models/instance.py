import typing as t
from . import Vertex


class Instance(t.NamedTuple):
    name: t.Optional[str]
    type: t.Optional[str]
    comment: t.Optional[str]
    dimension: int
    edge_weight_type: t.Optional[str]
    display_data_type: t.Optional[str]
    vertices: t.List[Vertex]
