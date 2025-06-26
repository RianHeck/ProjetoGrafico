import pygame
import numpy as np
from Mesh import Mesh
from Transformacao import gerar_matriz_composta, aplicar_em_vertices
from DisplayFile import File

# Configurações da janela
WIDTH, HEIGHT = 1280, 720
VIEWPORT_RECT = pygame.Rect(580, 20, 680, 680)
PAINEL1_RECT = pygame.Rect(20, 20, 260, 680)
PAINEL2_RECT = pygame.Rect(300, 20, 260, 680)
SRU = [-100, -100, 100, 100]  
SRD = [VIEWPORT_RECT.left, VIEWPORT_RECT.top, VIEWPORT_RECT.right, VIEWPORT_RECT.bottom]  # Espaço da tela

# Inicializa pygame
pygame.init()
tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Precisava Mesmo Disso?")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# Botoes da interface

botoes = {
    'Polígono': pygame.Rect(30, 30, 240, 40),
    'Circulo': pygame.Rect(30, 80, 240, 40),
    'Translação': pygame.Rect(30, 130, 240, 40),
    'Escala': pygame.Rect(30, 180, 240, 40),
    'Reflexão': pygame.Rect(30, 230, 240, 40),
    'Cisalhamento': pygame.Rect(30, 280, 240, 40),
    'Rotação': pygame.Rect(30, 330, 240, 40),
    'Importar': pygame.Rect(30, 380, 240, 40),
    #'Extra1': pygame.Rect(30, 430, 240, 40),
    #'Extra2': pygame.Rect(30, 480, 240, 40),
    #'Extra3': pygame.Rect(30, 530, 240, 40),
    'Confirmar': pygame.Rect(30, 580, 240, 40),
    'Cancelar': pygame.Rect(30, 630, 240, 40),
}

opcoes_transformacoes = {
    'Polígono': {'X': {'Valor': '', 'Rect': pygame.Rect(30, 430, 240, 40)}, 'Y': {'Valor': '', 'Rect': pygame.Rect(30, 480, 240, 40)}, 'Próximo': {'Rect': pygame.Rect(30, 530, 240, 40)}},
    'Circulo': {'X': {'Valor': '', 'Rect': pygame.Rect(30, 430, 240, 40)}, 'Y': {'Valor': '', 'Rect': pygame.Rect(30, 480, 240, 40)}, 'Raio': {'Valor': '', 'Rect': pygame.Rect(30, 530, 240, 40)}},
    'Translação': {'Dx': {'Valor': '', 'Rect': pygame.Rect(30, 430, 240, 40)}, 'Dy': {'Valor': '', 'Rect': pygame.Rect(30, 480, 240, 40)}},
    'Escala': {'Sx': {'Valor': '', 'Rect': pygame.Rect(30, 430, 240, 40)}, 'Sy': {'Valor': '', 'Rect': pygame.Rect(30, 480, 240, 40)}},
    'Reflexão': {'Eixo': {'Valor': '', 'Rect': pygame.Rect(30, 430, 240, 40)}},
    'Cisalhamento': {'Shx': {'Valor': '', 'Rect': pygame.Rect(30, 430, 240, 40)}, 'Shy': {'Valor': '', 'Rect': pygame.Rect(30, 480, 240, 40)}},
    'Rotação': {'Angulo': {'Valor': '', 'Rect': pygame.Rect(30, 430, 240, 40)}},
    'Importar': {'Arquivo': {'Valor': '', 'Rect': pygame.Rect(30, 430, 240, 40)}},
}


def desenhar_viewport(tela):
    for d in display_file:
        for f in d.mesh.faces:
            arestas = d.mesh.arestasDeUmaFace(f)
            for aresta in arestas:
                #aplicar transformação
                matriz = gerar_matriz_composta(d.transformacoes)
                v1 = aplicar_em_vertices(matriz, np.array([aresta.origem.posicao[0], aresta.origem.posicao[1], 1]))
                v2 = aplicar_em_vertices(matriz, np.array([aresta.proxima.origem.posicao[0], aresta.proxima.origem.posicao[1], 1]))
                pygame.draw.line(tela, (255, 255, 255), (v1[0] + VIEWPORT_RECT.left, v1[1] + VIEWPORT_RECT.top), (v2[0] + VIEWPORT_RECT.left, v2[1] + VIEWPORT_RECT.top), 2)
            
    

def desenhar_interface():
    pygame.draw.rect(tela, (50, 50, 50), PAINEL1_RECT, border_radius=10)
    pygame.draw.rect(tela, (50, 50, 50), PAINEL2_RECT, border_radius=10)
    pygame.draw.rect(tela, (20, 20, 20), VIEWPORT_RECT)
    for nome, rect in botoes.items():
        if nome == opcao_selecionada:
            pygame.draw.rect(tela, (70, 70, 70), rect, border_radius=6)
        else:
            pygame.draw.rect(tela, (100, 100, 100), rect, border_radius=6)
        texto = font.render(nome.upper(), True, (255, 255, 255))
        tela.blit(texto, (rect.x + 10, rect.y + 10))
    for i, mesh in enumerate(display_file):
        if i == mesh_selecionada:
            pygame.draw.rect(tela, (70, 70, 70), (310, 30 + 50 * i, 240, 40), border_radius=6)
        else:
            pygame.draw.rect(tela, (100, 100, 100), (310, 30 + 50 * i, 240, 40), border_radius=6)
        texto = font.render(f"Mesh {i + 1}", True, (255, 255, 255))
        tela.blit(texto, (320, 30 + 50 * i + 10))
    if opcao_selecionada:
        for i in opcoes_transformacoes[opcao_selecionada].keys():
            if i == 'Arquivo':
                if caixa_selecionada == i:
                    #podia usar o rect dnv
                    pygame.draw.rect(tela, (70, 70, 70), pygame.Rect(30, 430 + list(opcoes_transformacoes[opcao_selecionada].keys()).index(i) * 50, 240, 40), border_radius=6)
                else:
                    # não tava usando pq n ia criar
                    pygame.draw.rect(tela, (100, 100, 100), pygame.Rect(30, 430 + list(opcoes_transformacoes[opcao_selecionada].keys()).index(i) * 50, 240, 40), border_radius=6)
                texto = font.render(f"{i}: {opcoes_transformacoes[opcao_selecionada][i]['Valor']}", True, (255, 255, 255))
                tela.blit(texto, (40, 440))
            else:
                if caixa_selecionada == i:
                    pygame.draw.rect(tela, (70, 70, 70), pygame.Rect(30, 430 + list(opcoes_transformacoes[opcao_selecionada].keys()).index(i) * 50, 240, 40), border_radius=6)
                else:
                    pygame.draw.rect(tela, (100, 100, 100), pygame.Rect(30, 430 + list(opcoes_transformacoes[opcao_selecionada].keys()).index(i) * 50, 240, 40), border_radius=6)
                if 'Valor' in opcoes_transformacoes[opcao_selecionada][i].keys(): 
                    texto = font.render(f"{i}: {opcoes_transformacoes[opcao_selecionada][i]['Valor']}", True, (255, 255, 255))
                    tela.blit(texto, (40, 440 + list(opcoes_transformacoes[opcao_selecionada].keys()).index(i) * 50))
                else: 
                    texto = font.render(i, True, (255, 255, 255))
                    tela.blit(texto, (40, 440 + list(opcoes_transformacoes[opcao_selecionada].keys()).index(i) * 50))
        
def criar_forma(nome):
    m = Mesh()
    if nome == "quadrado":
        m.vertices = [
            type('V', (), {'posicao': (-5, -5, 0)}),
            type('V', (), {'posicao': (5, -5, 0)}),
            type('V', (), {'posicao': (5, 5, 0)}),
            type('V', (), {'posicao': (-5, 5, 0)})
        ]
    elif nome == "triangulo":
        m.vertices = [
            type('V', (), {'posicao': (-5, -5, 0)}),
            type('V', (), {'posicao': (5, -5, 0)}),
            type('V', (), {'posicao': (0, 5, 0)})
        ]
    f = type('F', (), {})()
    f.id = 1
    a = type('A', (), {})()
    a.id = 1
    f.aresta = a
    m.faces = [f]
    m.arestasDeUmaFace = lambda f: [[type('A', (), {'origem': v}) for v in m.vertices]]
    return m


def centro_mesh(display_item):
    """Calcula o centro atual da mesh sem considerar a transformacao de viewport."""
    if not display_item.mesh.vertices:
        return 0, 0
    vertices = [
        [v.posicao[0], v.posicao[1], 1] for v in display_item.mesh.vertices
    ]
    # Transforma os vertices com as transformacoes aplicadas, exceto viewport
    transformacoes = [t for t in display_item.transformacoes if t[0] != 'viewport']
    if transformacoes:
        matriz = gerar_matriz_composta(transformacoes)
        pts = aplicar_em_vertices(matriz, np.array(vertices))
    else:
        pts = np.array(vertices)
    cx = float(np.mean(pts[:, 0]))
    cy = float(np.mean(pts[:, 1]))
    return cx, cy

def main():
    global display_file
    global opcao_selecionada
    global caixa_selecionada
    global mesh_selecionada
    caixa_selecionada = None
    opcao_selecionada = None
    mesh_selecionada = None
    display_file = []
    modo = None
    
    site = Mesh()
    site.abrirOBJ('Site.obj')
    file = File(site)
    #file = File(Mesh().abrirOBJ('Site.obj'))
    #file.transformacoes.append(('scale', 0.5, 0.5))
    #file.transformacoes.append(('translation', 1, 1))
    display_file.append(file)
    
    file2 = File(Mesh())
    display_file.append(file2)
    
    running = True
    while running:
        tela.fill((25, 25, 25))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if PAINEL1_RECT.collidepoint(mx, my):
                    for nome, rect in botoes.items():
                        if rect.collidepoint(mx, my):
                            if modo != nome:
                                caixa_selecionada = None
                            if nome != 'Confirmar':
                                modo = nome
                            if modo == 'Polígono':
                                opcao_selecionada = 'Polígono'
                            elif modo == 'Circulo':
                                opcao_selecionada = 'Circulo'
                            elif modo == 'Translação':
                                opcao_selecionada = 'Translação'
                            elif modo == 'Escala':
                                opcao_selecionada = 'Escala'
                            elif modo == 'Reflexão':
                                opcao_selecionada = 'Reflexão'
                            elif modo == 'Cisalhamento':
                                opcao_selecionada = 'Cisalhamento'
                            elif modo == 'Rotação':
                                opcao_selecionada = 'Rotação'
                            elif modo == 'Importar':
                                opcao_selecionada = 'Importar'
                            if nome == 'Confirmar':
                                if mesh_selecionada is not None and opcao_selecionada:
                                    match opcao_selecionada:
                                        case 'Translação':
                                            if (opcoes_transformacoes[opcao_selecionada]['Dx']['Valor'] and
                                                opcoes_transformacoes[opcao_selecionada]['Dy']['Valor']):
                                                dx = float(opcoes_transformacoes[opcao_selecionada]['Dx']['Valor'])
                                                dy = float(opcoes_transformacoes[opcao_selecionada]['Dy']['Valor'])
                                                display_file[mesh_selecionada].transformacoes.append(('translation', dx, dy))
                                        case 'Escala':
                                            if (opcoes_transformacoes[opcao_selecionada]['Sx']['Valor'] and
                                                opcoes_transformacoes[opcao_selecionada]['Sy']['Valor']):
                                                sx = float(opcoes_transformacoes[opcao_selecionada]['Sx']['Valor'])
                                                sy = float(opcoes_transformacoes[opcao_selecionada]['Sy']['Valor'])
                                                #ERRO Ainda Não Entedi Pq Mas É Assim
                                                cx, cy = centro_mesh(display_file[mesh_selecionada])
                                                cx, cy = display_file[mesh_selecionada].centro_original
                                                display_file[mesh_selecionada].transformacoes.extend([
                                                    ('translation', cx, cy),
                                                    ('scale', sx, sy),
                                                    ('translation', -cx, -cy)
                                                ])
                                        case 'Reflexão':
                                            if opcoes_transformacoes[opcao_selecionada]['Eixo']['Valor']:
                                                eixo = opcoes_transformacoes[opcao_selecionada]['Eixo']['Valor']
                                                #ERRO Ainda Não Entedi Pq Mas É Assim
                                                cx, cy = centro_mesh(display_file[mesh_selecionada])
                                                cx, cy = display_file[mesh_selecionada].centro_original
                                                display_file[mesh_selecionada].transformacoes.extend([
                                                    ('translation', cx, cy),
                                                    ('reflection', eixo),
                                                    ('translation', -cx, -cy)
                                                ])
                                        case 'Cisalhamento':
                                            if (opcoes_transformacoes[opcao_selecionada]['Shx']['Valor'] and
                                                opcoes_transformacoes[opcao_selecionada]['Shy']['Valor']):
                                                shx = float(opcoes_transformacoes[opcao_selecionada]['Shx']['Valor'])
                                                shy = float(opcoes_transformacoes[opcao_selecionada]['Shy']['Valor'])
                                                #ERRO Ainda Não Entedi Pq Mas É Assim
                                                cx, cy = centro_mesh(display_file[mesh_selecionada])
                                                cx, cy = display_file[mesh_selecionada].centro_original
                                                display_file[mesh_selecionada].transformacoes.extend([
                                                    ('translation', cx, cy),
                                                    ('shearing', shx, shy),
                                                    ('translation', -cx, -cy)
                                                ])
                                        case 'Rotação':
                                            if opcoes_transformacoes[opcao_selecionada]['Angulo']['Valor']:
                                                ang = float(opcoes_transformacoes[opcao_selecionada]['Angulo']['Valor'])
                                                #ERRO Ainda Não Entedi Pq Mas É Assim
                                                cx, cy = centro_mesh(display_file[mesh_selecionada])
                                                cx, cy = display_file[mesh_selecionada].centro_original
                                                display_file[mesh_selecionada].transformacoes.extend([
                                                    ('translation', cx, cy),
                                                    ('rotation', ang),
                                                    ('translation', -cx, -cy)
                                                ])
                                    #Mais Cliques Mais Trabalho
                                    #opcao_selecionada = None
                                    #caixa_selecionada = None
                                    #mesh_selecionada = None
                                    #modo = None
                            elif modo == 'Cancelar':
                                opcao_selecionada = None
                                caixa_selecionada = None
                                modo = None
                    if opcao_selecionada:
                        for nome, dict in opcoes_transformacoes[opcao_selecionada].items():
                            rect = dict['Rect']
                            if rect.collidepoint(mx, my):
                                caixa_selecionada = nome
                elif PAINEL2_RECT.collidepoint(mx, my):
                    for i, mesh in enumerate(display_file):
                        if pygame.Rect(310, 30 + 50 * i, 240, 40).collidepoint(mx, my):
                            mesh_selecionada = i               
            elif event.type == pygame.KEYDOWN:
                if event.key == 99:  # 'c' key
                    if mesh_selecionada is not None:
                        print(f'Centro da mesh {mesh_selecionada + 1}: {centro_mesh(display_file[mesh_selecionada])}')
                if event.key == 116: # 't' key
                    if mesh_selecionada is not None:
                        print(f'Transformações da mesh {mesh_selecionada + 1}: {display_file[mesh_selecionada].transformacoes}')
                if event.key == pygame.K_ESCAPE:
                    opcao_selecionada = None
                    caixa_selecionada = None
                    mesh_selecionada = None
                elif caixa_selecionada:
                    if event.key == pygame.K_BACKSPACE:
                        if opcoes_transformacoes[opcao_selecionada][caixa_selecionada]['Valor'] is not None:
                            stringatual = opcoes_transformacoes[opcao_selecionada][caixa_selecionada]['Valor']
                            opcoes_transformacoes[opcao_selecionada][caixa_selecionada]['Valor'] = stringatual[:-1]
                    if caixa_selecionada in ['X', 'Y', 'Raio', 'Dx', 'Dy', 'Sx', 'Sy', 'Shx', 'Shy', 'Angulo']:
                        valor_atual = opcoes_transformacoes[opcao_selecionada][caixa_selecionada]['Valor'] or ''
                        if (event.unicode.isdigit() or
                            (event.unicode == '.' and '.' not in valor_atual) or
                            (event.unicode == '-' and valor_atual == '')):
                            if len(valor_atual) < 10:
                                opcoes_transformacoes[opcao_selecionada][caixa_selecionada]['Valor'] = valor_atual + event.unicode
                    if caixa_selecionada == 'Eixo':
                        if event.unicode.lower() in ['x', 'y']:
                            opcoes_transformacoes[opcao_selecionada][caixa_selecionada]['Valor'] = event.unicode.lower()
                    if caixa_selecionada == 'Arquivo':
                        if event.unicode.isalnum() or event.unicode in ['.', '_']:
                            if opcoes_transformacoes[opcao_selecionada][caixa_selecionada]['Valor'] is None:
                                opcoes_transformacoes[opcao_selecionada][caixa_selecionada]['Valor'] = event.unicode
                            else:
                                if len(opcoes_transformacoes[opcao_selecionada][caixa_selecionada]['Valor']) < 50:
                                    stringatual = opcoes_transformacoes[opcao_selecionada][caixa_selecionada]['Valor']
                                    opcoes_transformacoes[opcao_selecionada][caixa_selecionada]['Valor'] = stringatual + event.unicode

        desenhar_interface()
        desenhar_viewport(tela)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
