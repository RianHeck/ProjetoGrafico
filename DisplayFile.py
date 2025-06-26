from Mesh import Mesh

class File:
    def __init__(self, mesh: Mesh):
        self.mesh = mesh
        if mesh.vertices:
            Xmin = min(v.posicao[0] for v in mesh.vertices)
            Xmax = max(v.posicao[0] for v in mesh.vertices)
            Ymin = min(v.posicao[1] for v in mesh.vertices)
            Ymax = max(v.posicao[1] for v in mesh.vertices)
            self.window = (Xmin, Ymin, Xmax, Ymax)
            self.transformacoes = [('viewport', (self.window), (0, 0, 680, 680))]
        else:
            self.transformacoes = [('viewport', (-100, -100, 100, 100), (0, 0, 680, 680))]


        