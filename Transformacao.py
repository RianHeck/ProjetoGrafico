# Joao Pedro Correa Crozariolo 
# Rian Augusto Heck
import numpy as np

# ------ TRANSFORMACOES 2D ------ #
def transform_2d(matrix, tipo, *params):
    """
    Aplica uma transformação 2D sobre uma matriz acumulada.
    """
    if tipo == 'translation':
        dx, dy = params
        # Matriz de translacao em 2D
        t = np.array([[1, 0, dx],
                      [0, 1, dy],
                      [0, 0, 1]])
    elif tipo == 'scale':
        sx, sy = params
        # Matriz de escala em 2D
        t = np.array([[sx, 0, 0],
                      [0, sy, 0],
                      [0, 0, 1]])
    elif tipo == 'reflection':
        eixo = params[0]
        # Reflexao sobre o eixo X
        if eixo == 'x':
            t = np.array([[1, 0, 0],
                          [0, -1, 0],
                          [0, 0, 1]])
        # Reflexao sobre o eixo Y
        elif eixo == 'y':
            t = np.array([[-1, 0, 0],
                          [0, 1, 0],
                          [0, 0, 1]])
    elif tipo == 'shearing':
        shx, shy = params
        # Cisalhamento (shear) em 2D
        t = np.array([[1, shx, 0],
                      [shy, 1, 0],
                      [0, 0, 1]])
    elif tipo == 'rotation':
        ang = np.radians(params[0])  # Converte o angulo para radianos
        # Rotacao em torno da origem
        t = np.array([[np.round(np.cos(ang)), np.round(-np.sin(ang)), 0],
                      [np.round(np.sin(ang)), np.round(np.cos(ang)), 0],
                      [0, 0, 1]])
    else:
        raise ValueError(f"Transformação 2D '{tipo}' não reconhecida.")

    return np.dot(t, matrix)  # Aplica a transformacao sobre a matriz acumulada

# ------ TRANSFORMACOES 3D ------ #
def transform_3d(matrix, tipo, *params):
    """
    Aplica uma transformação 3D sobre uma matriz acumulada.
    """
    if tipo == 'translation':
        dx, dy, dz = params
        # Matriz de translacao em 3D
        t = np.array([[1, 0, 0, dx],
                      [0, 1, 0, dy],
                      [0, 0, 1, dz],
                      [0, 0, 0, 1]])
    elif tipo == 'scale':
        sx, sy, sz = params
        # Matriz de escala em 3D
        t = np.array([[sx, 0, 0, 0],
                      [0, sy, 0, 0],
                      [0, 0, sz, 0],
                      [0, 0, 0, 1]])
    elif tipo == 'reflection':
        plano = params[0]
        # Reflexao em planos principais
        if plano == 'xy':
            t = np.diag([1, 1, -1, 1])
        elif plano == 'xz':
            t = np.diag([1, -1, 1, 1])
        elif plano == 'yz':
            t = np.diag([-1, 1, 1, 1])
    elif tipo == 'shearing':
        eixo, v1, v2 = params
        # Matriz identidade como base
        t = np.eye(4)
        # Cisalhamento em relacao ao eixo selecionado
        if eixo == 'x':
            t[0][1] = v1
            t[0][2] = v2
        elif eixo == 'y':
            t[1][0] = v1
            t[1][2] = v2
        elif eixo == 'z':
            t[2][0] = v1
            t[2][1] = v2
    elif tipo == 'rotation':
        eixo, ang = params
        ang = np.radians(ang)
        # Rotacao em torno do eixo X
        if eixo == 'x':
            t = np.array([[1, 0, 0, 0],
                          [0, np.cos(ang), -np.sin(ang), 0],
                          [0, np.sin(ang),  np.cos(ang), 0],
                          [0, 0, 0, 1]])
        # Rotacao em torno do eixo Y
        elif eixo == 'y':
            t = np.array([[np.cos(ang), 0, np.sin(ang), 0],
                          [0, 1, 0, 0],
                          [-np.sin(ang), 0, np.cos(ang), 0],
                          [0, 0, 0, 1]])
        # Rotacao em torno do eixo Z
        elif eixo == 'z':
            t = np.array([[np.cos(ang), -np.sin(ang), 0, 0],
                          [np.sin(ang),  np.cos(ang), 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])
    else:
        raise ValueError(f"Transformação 3D '{tipo}' não reconhecida.")

    return np.dot(t, matrix)

# ------ MENU DE COLETA DE TRANSFORMACOES ------ #
def coletar_transformacoes():
    """
    Interface de texto para coletar uma sequência de transformações do usuário.
    """
    print("# ------ Sistema de Transformações Gráficas ------ #")
    dim = input("Escolha a dimensão (2d/3d): ").strip().lower()
    while dim not in ['2d', '3d']:
        dim = input("Entrada inválida. Digite '2d' ou '3d': ").strip().lower()

    transformacoes = []

    # Mapeamento das opcoes
    opcoes = {
        "1": "translation",
        "2": "scale",
        "3": "reflection",
        "4": "shearing",
        "5": "rotation",
        "6": "finalizar"
    }

    # Loop de coleta
    while True:
        print("\nTransformações disponíveis:")
        for k, v in opcoes.items():
            print(f"{k} - {v.capitalize()}")
        escolha = input("Digite o número da transformação desejada: ").strip()
        if escolha == "6":
            break
        tipo = opcoes.get(escolha)
        if not tipo:
            print("Opção inválida.")
            continue

        # Leitura dos parametros de cada tipo de transformacao
        try:
            if tipo == "translation":
                dx = float(input("dx: "))
                dy = float(input("dy: "))
                if dim == '3d':
                    dz = float(input("dz: "))
                    transformacoes.append((tipo, dx, dy, dz))
                else:
                    transformacoes.append((tipo, dx, dy))
            elif tipo == "scale":
                sx = float(input("sx: "))
                sy = float(input("sy: "))
                if dim == '3d':
                    sz = float(input("sz: "))
                    transformacoes.append((tipo, sx, sy, sz))
                else:
                    transformacoes.append((tipo, sx, sy))
            elif tipo == "reflection":
                eixo = input("Eixo ou plano (x, y, xy, xz, yz): ").strip().lower()
                transformacoes.append((tipo, eixo))
            elif tipo == "shearing":
                if dim == '2d':
                    shx = float(input("shx: "))
                    shy = float(input("shy: "))
                    transformacoes.append((tipo, shx, shy))
                else:
                    eixo = input("Eixo de cisalhamento (x, y, z): ").strip().lower()
                    v1 = float(input("Parâmetro 1: "))
                    v2 = float(input("Parâmetro 2: "))
                    transformacoes.append((tipo, eixo, v1, v2))
            elif tipo == "rotation":
                if dim == '2d':
                    ang = float(input("Ângulo (graus): "))
                    transformacoes.append((tipo, ang))
                else:
                    eixo = input("Eixo de rotação (x, y, z): ").strip().lower()
                    ang = float(input("Ângulo (graus): "))
                    transformacoes.append((tipo, eixo, ang))
        except ValueError:
            print("Erro: todos os valores devem ser numéricos.")

    return dim, transformacoes

# ------ GERACAO DA MATRIZ COMPOSTA ------ #
def gerar_matriz_composta(dim, transformacoes):
    """
    Gera a matriz de transformação composta aplicando as transformações na ordem reversa.
    """
    matriz = np.eye(3) if dim == '2d' else np.eye(4)
    for t in reversed(transformacoes):  # Ordem inversa (ultima definida e aplicada primeiro)
        tipo, *params = t
        if dim == '2d':
            matriz = transform_2d(matriz, tipo, *params)
        else:
            matriz = transform_3d(matriz, tipo, *params)
    return matriz

# ------ APLICA A MATRIZ EM VERTICES ------ #
def aplicar_em_vertices(matriz, vertices):
    """
    Aplica a matriz de transformação sobre uma lista de vértices.
    """
    return np.dot(vertices, matriz.T)

# ------ PROGRAMA PRINCIPAL ------ #
def main():
    # Coleta da dimensao e transformacoes desejadas
    dim, transformacoes = coletar_transformacoes()

    print("\nTransformações definidas:")
    for i, t in enumerate(transformacoes, 1):
        print(f"{i}. {t}")

    # Geracao da matriz final composta
    matriz_final = gerar_matriz_composta(dim, transformacoes)
    print("\nMatriz composta final:")
    print(matriz_final)

    # Exemplo de aplicacao: transforma o ponto (1, 1) ou (1, 1, 1)
    if dim == '2d':
        vertices = np.array([[1, 1, 1]])
    else:
        vertices = np.array([[1, 1, 1, 1]])

    #print("\nAplicando a matriz ao ponto:")
    #print(f"Antes: {vertices}")
    #print("Depois:", aplicar_em_vertices(matriz_final, vertices))

# Execucao principal
if __name__ == "__main__":
    main()
