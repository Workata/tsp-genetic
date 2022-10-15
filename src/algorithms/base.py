from abc import abstractmethod, ABC
import typing as t
from utils import Calculator, AdjencyMatrixCreator
from models import Vertex
from loaders import InstanceLoader


class BaseTspSolver(ABC):

    def __init__(self):
        self._instance_loader = InstanceLoader()
        self._calculator = Calculator()
        self._matrix_creator = AdjencyMatrixCreator(calculator=self._calculator)

    @abstractmethod
    def solve(self) -> t.Tuple[int, t.List[Vertex]]:
        pass
