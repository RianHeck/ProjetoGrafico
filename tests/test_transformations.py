import numpy as np
import pytest

from Transformacao import gerar_matriz_composta, aplicar_em_vertices


def center_of(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return sum(xs) / len(xs), sum(ys) / len(ys)


@pytest.mark.parametrize(
    "points",
    [
        [(-1, -1), (1, -1), (1, 1), (-1, 1)],  # square
        [(-1, -1), (1, -1), (0, 1)],          # triangle
    ],
)
def test_rotation_preserves_center(points):
    cx, cy = center_of(points)
    angle = 45
    transformacoes = [
        ("translation", cx, cy),
        ("rotation", angle),
        ("translation", -cx, -cy),
    ]
    matriz = gerar_matriz_composta(transformacoes)
    verts = np.array([[x, y, 1] for x, y in points])
    transformed = aplicar_em_vertices(matriz, verts)
    new_cx, new_cy = center_of([row[:2] for row in transformed])
    assert np.allclose([cx, cy], [new_cx, new_cy])
