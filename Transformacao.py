import numpy as np

def transform_2d(matrix, tipo, *params):
    if tipo == 'translation':
        dx, dy = params
        t = np.array([[1, 0, dx],
                      [0, 1, dy],
                      [0, 0, 1]])
    elif tipo == 'scale':
        sx, sy = params
        t = np.array([[sx, 0, 0],
                      [0, sy, 0],
                      [0, 0, 1]])
    elif tipo == 'reflection':
        eixo = params[0]
        if eixo == 'x':
            t = np.array([[1, 0, 0],
                          [0, -1, 0],
                          [0, 0, 1]])
        elif eixo == 'y':
            t = np.array([[-1, 0, 0],
                          [0, 1, 0],
                          [0, 0, 1]])
    elif tipo == 'shearing':
        shx, shy = params
        t = np.array([[1, shx, 0],
                      [shy, 1, 0],
                      [0, 0, 1]])
    elif tipo == 'rotation':
        ang = np.radians(params[0])
        t = np.array([[np.round(np.cos(ang)), np.round(-np.sin(ang)), 0],
                      [np.round(np.sin(ang)), np.round(np.cos(ang)), 0],
                      [0, 0, 1]])
    elif tipo == 'viewport':
        sru = params[0]
        srd = params[1]
        t = np.array([
            [(srd[2] - srd[0]) / (sru[2] - sru[0]), 0, srd[0] - sru[0] * (srd[2] - srd[0]) / (sru[2] - sru[0])],
            [0, (srd[3] - srd[1]) / (sru[3] - sru[1]), srd[1] - sru[1] * (srd[3] - srd[1]) / (sru[3] - sru[1])],
            [0, 0, 1]
        ])
    else:
        raise ValueError(f"Transformação 2D '{tipo}' não reconhecida.")

    return np.dot(t, matrix)




def gerar_matriz_composta(transformacoes):
    matriz = np.eye(3)
    for t in reversed(transformacoes):
        tipo, *params = t
        matriz = transform_2d(matriz, tipo, *params)
    return matriz





def aplicar_em_vertices(matriz, vertices):
    return np.dot(vertices, matriz.T)
