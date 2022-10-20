import numpy as np
import pytest
from models import Instance, Vertex
from utils import AdjencyMatrixCreator, Calculator

# TODO add recipe

@pytest.fixture
def matrix_creator():
    return AdjencyMatrixCreator(Calculator())


@pytest.fixture
def vertices_1():
    return [
        Vertex(1, x=0, y=0),
        Vertex(2, x=3, y=0),
        Vertex(3, x=3, y=4),
    ]

@pytest.fixture
def vertices_2():
    return [
        Vertex(1, x=-5, y=-5),
        Vertex(2, x=-2, y=-5),
        Vertex(3, x=-2, y=-1)
    ]

@pytest.fixture
def vertices_3():
    return [
        Vertex(1, x=-2, y=1),
        Vertex(2, x=1, y=1),
        Vertex(3, x=1, y=5),
    ]

@pytest.fixture
def vertices_4():
    return [
        Vertex(1, x=-2.5, y=1.5),
        Vertex(2, x=0.5, y=1.5),
        Vertex(3, x=0.5, y=5.5),
    ]

@pytest.fixture
def instance_1(vertices_1):
    return Instance(
        name='',
        type='',
        comment='',
        edge_weight_type='',
        display_data_type='',
        dimension=3,
        vertices=vertices_1
    )

@pytest.fixture
def instance_2(vertices_2):
    return Instance(
        name='',
        type='',
        comment='',
        edge_weight_type='',
        display_data_type='',
        dimension=3,
        vertices=vertices_2
    )


@pytest.fixture
def instance_3(vertices_3):
    return Instance(
        name='',
        type='',
        comment='',
        edge_weight_type='',
        display_data_type='',
        dimension=3,
        vertices=vertices_3
    )

@pytest.fixture
def instance_4(vertices_4):
    return Instance(
        name='',
        type='',
        comment='',
        edge_weight_type='',
        display_data_type='',
        dimension=3,
        vertices=vertices_4
    )

def test_adj_matrix_creation_from_positive_coords(matrix_creator, instance_1):
    expected_matrix = np.array([
        [0, 0, 0, 0],
        [0, 0, 3, 5],
        [0, 3, 0, 4],
        [0, 5, 4, 0],
    ], dtype=float)

    adj_matrix = matrix_creator.create(instance_1)
    np.testing.assert_array_equal(expected_matrix, adj_matrix)


def test_adj_matrix_creation_from_negative_coords(matrix_creator, instance_2):
    expected_matrix = np.array([
        [0, 0, 0, 0],
        [0, 0, 3, 5],
        [0, 3, 0, 4],
        [0, 5, 4, 0],
    ], dtype=float)

    adj_matrix = matrix_creator.create(instance_2)
    np.testing.assert_array_equal(expected_matrix, adj_matrix)


def test_adj_matrix_creation_from_mixed_coords(matrix_creator, instance_3):
    expected_matrix = np.array([
        [0, 0, 0, 0],
        [0, 0, 3, 5],
        [0, 3, 0, 4],
        [0, 5, 4, 0],
    ], dtype=float)

    adj_matrix = matrix_creator.create(instance_3)
    np.testing.assert_array_equal(expected_matrix, adj_matrix)


def test_adj_matrix_creation_from_mixed_float_coords(matrix_creator, instance_4):
    expected_matrix = np.array([
        [0, 0, 0, 0],
        [0, 0, 3, 5],
        [0, 3, 0, 4],
        [0, 5, 4, 0],
    ], dtype=float)

    adj_matrix = matrix_creator.create(instance_4)
    np.testing.assert_array_equal(expected_matrix, adj_matrix)


