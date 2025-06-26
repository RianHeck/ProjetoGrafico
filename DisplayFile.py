from Mesh import Mesh
import numpy as np

class File:
    def __init__(self, mesh: Mesh):
        self.mesh = mesh
        if mesh.vertices:
            Xmin = min(v.posicao[0] for v in mesh.vertices)
            Xmax = max(v.posicao[0] for v in mesh.vertices)
            Ymin = min(v.posicao[1] for v in mesh.vertices)
            Ymax = max(v.posicao[1] for v in mesh.vertices)
            vertices = [[v.posicao[0], v.posicao[1], 1] for v in self.mesh.vertices]
            pts = np.array(vertices)
            cx = float(np.mean(pts[:, 0]))
            cy = float(np.mean(pts[:, 1]))
            self.centro_original = (cx, cy)
            self.window = (Xmin, Ymin, Xmax, Ymax)
            self.transformacoes = [('viewport', (self.window), (0, 0, 680, 680))]
        else:
            self.transformacoes = [('viewport', (-100, -100, 100, 100), (0, 0, 680, 680))]


        