class Vertice:
    def __init__(self, id, posicao):
        self.id = id
        self.posicao = posicao  # (x, y, z)
        self.arestaIncidente = None 
        
    def __str__(self):
        return f"Vertice(ID: {self.id}, Posição: {self.posicao}, Aresta Incidente: {self.arestaIncidente.id if self.arestaIncidente else 'None'})"
    
    def __repr__(self):
        return f"Vertice(ID: {self.id})"

class HalfEdge:
    def __init__(self):
        self.origem = None
        self.gemea = None      
        self.faceIncidente = None 
        self.proxima = None
        self.anterior = None
        self.id = None  # Apenas Pra debugar, não é necessário para o funcionamento do código

    def __str__(self):
        id_str = f"({self.id})" if self.id else "None"
        origem_str = str(self.origem.id) if self.origem else "None"
        gemea_str = f"({(self.gemea.id)} -> {self.gemea.origem.id})" if self.gemea else "None"
        face_str = f"({self.faceIncidente.id})" if self.faceIncidente else "None"
        proxima_str = f"({(self.proxima.id)})" if self.proxima else "None"
        anterior_str = f"({(self.anterior.id)})" if self.anterior else "None"
        return f"HalfEdge(Id: {id_str}, Origem: {origem_str}, Gêmea: {gemea_str}, Face Incidente: {face_str}, Próxima: {proxima_str}, Anterior: {anterior_str})"
    
    def __repr__(self):
        return f"Aresta(ID: {self.id})"
    
class Face:
    def __init__(self, id):
        self.id = id
        self.aresta = None
    
    def __str__(self):
        return f"Face(ID: {self.id}, Aresta Incidente: {self.aresta.id})"
    
    def __repr__(self):
        return f"Face(ID: {self.id})"


class Mesh:
    def __init__(self):
        self.vertices = []
        self.arestas = []
        self.faces = []
        
    def halfEdgeName(self, aresta):
        return f"HalfEdge {aresta.id}"
        
    def __str__(self):
        vertices_str = "\n".join(str(v) for v in self.vertices)
        arestas_str = "\n".join(str(a) for a in self.arestas)
        faces_str = "\n".join(str(f) for f in self.faces)
        return f"Mesh:\n\nVértices:\n{vertices_str}\n\nArestas:\n{arestas_str}\n\nFaces:\n{faces_str}"
        
    def printar(self):
        print("Vértices:")
        for vertice in self.vertices:
            print(vertice)
        print("\nArestas:")
        for aresta in self.arestas:
            print(aresta)
        print("\nFaces:")
        for face in self.faces:
            print(face)

    def abrirOBJ(self, caminho):
        with open(caminho, 'r') as arquivo:
            linhas = arquivo.readlines()
        for linha in linhas:
            if linha.startswith('#'): # ignora comentários
                continue
            elif linha.startswith('v '): # linha de vértice
                partes = linha.split()
                x, y, z = map(float, partes[1:4])
                vertice = Vertice((len(self.vertices) + 1), (x, y, z))
                self.vertices.append(vertice)
            elif linha.startswith('f '):
                partes = linha.split()
                face = Face((len(self.faces) + 1))
                indicesVerticesFace = []
                for i in range(1, len(partes)):
                    indiceVertice = int(partes[i].split('/')[0])
                    indicesVerticesFace.append(indiceVertice)
                indiceVerticeAnterior = None
                indicePrimeiroVertice = None
                primeiraAresta = None
                arestaAnterior = None
                for i, indice in enumerate(indicesVerticesFace):
                    if i == 0:
                        indicePrimeiroVertice = indice
                    else:
                        aresta1, aresta2 = None, None
                        for aresta in self.arestas:
                            if aresta.origem.id == indiceVerticeAnterior and aresta.gemea.origem.id == indice:
                                aresta1 = aresta
                                aresta2 = aresta.gemea
                                break
                        if aresta1 is None and aresta2 is None:
                            aresta1 = HalfEdge()
                            aresta2 = HalfEdge()
                            aresta1.id = len(self.arestas) + 1
                            self.arestas.append(aresta1)
                            aresta2.id = len(self.arestas) + 1
                            self.arestas.append(aresta2)
                            #aresta1.id = self.arestas.append((len(self.arestas) + 1))
                            #aresta2.id = self.arestas.append((len(self.arestas) + 1))
                            aresta1.origem = self.vertices[indiceVerticeAnterior -1]
                            aresta2.origem = self.vertices[indice - 1]
                            aresta1.gemea = aresta2
                            aresta2.gemea = aresta1
                        aresta1.faceIncidente = face
                        if self.vertices[indiceVerticeAnterior - 1].arestaIncidente is None:
                            self.vertices[indiceVerticeAnterior - 1].arestaIncidente = aresta1
                        if i == len(indicesVerticesFace) - 1:
                            aresta3, aresta4 = None, None
                            for aresta in self.arestas:
                                if aresta.origem.id == indice and aresta.gemea.origem.id == indicePrimeiroVertice:
                                    aresta3 = aresta
                                    aresta4 = aresta.gemea
                                    break
                            if aresta3 is None and aresta4 is None:
                                aresta3 = HalfEdge()
                                aresta4 = HalfEdge()
                                aresta3.id = len(self.arestas) + 1
                                self.arestas.append(aresta3)
                                aresta4.id = len(self.arestas) + 1
                                self.arestas.append(aresta4)
                                #aresta3.id = self.arestas.append((len(self.arestas) + 1))
                                #aresta4.id = self.arestas.append((len(self.arestas) + 1))
                                aresta3.origem = self.vertices[indice - 1]
                                aresta4.origem = self.vertices[indicePrimeiroVertice - 1]
                                aresta3.gemea = aresta4
                                aresta4.gemea = aresta3
                            aresta3.faceIncidente = face
                            aresta1.proxima = aresta3
                            aresta3.anterior = aresta1
                            aresta3.proxima = primeiraAresta
                            primeiraAresta.anterior = aresta3
                            if self.vertices[indice - 1].arestaIncidente is None: #Tbm podia ignorar essa verificação e ir atualizando
                                self.vertices[indice - 1].arestaIncidente = aresta3
                            
                        if i == 1:
                            primeiraAresta = aresta1
                            face.aresta = aresta1
                            self.faces.append(face)
                        else:
                            arestaAnterior.proxima = aresta1
                            aresta1.anterior = arestaAnterior
                        arestaAnterior = aresta1
                    indiceVerticeAnterior = indice
                    #acho que teoricamente deve funcionar, mas não lida com casos de aresta.proxima e aresta.anterior de arestas externas
    
    def cicloExterno(self):
        primeiraAresta = None
        for aresta in self.arestas:
            if aresta.faceIncidente is None:
                primeiraAresta = aresta     
                break
        if primeiraAresta is None: #caso seja um mesh fechado
            return
        aresta = None
        ultimaAresta = None
        while aresta is not primeiraAresta:
            if aresta is None:
                aresta = primeiraAresta
            possivelProxima = aresta.gemea.anterior.gemea
            while possivelProxima.faceIncidente != None:
                possivelProxima = possivelProxima.anterior.gemea
            aresta.proxima = possivelProxima
            possivelProxima.anterior = aresta
            ultimaAresta = aresta
            aresta = possivelProxima
        primeiraAresta.anterior = ultimaAresta
            
    
    
    def facesDeUmVertice(self, vertice):
        primeraAresta = vertice.arestaIncidente
        faces = []
        aresta = None
        while aresta is not primeraAresta:
            if aresta == None:
                aresta = primeraAresta
            if aresta.faceIncidente != None:
                faces.append(aresta.faceIncidente)
            aresta = aresta.gemea.proxima
        return faces    
            
    def arestasDeUmVertice(self, vertice):
        primeiraAresta = vertice.arestaIncidente
        arestas = []
        aresta = None
        while aresta is not primeiraAresta:
            if aresta == None:
                aresta = primeiraAresta
            arestas.append(aresta)
            aresta = aresta.gemea.proxima
        return arestas
     
    def facesDeUmaAresta(self, aresta):
        return [aresta.faceIncidente] if aresta.faceIncidente else []
    
    def arestasDeUmaFace(self, face):
        primeiraAresta = face.aresta
        aresta = None
        arestas = []
        while aresta is not primeiraAresta:
            if aresta == None:
                aresta = primeiraAresta
            arestas.append(aresta)
            aresta = aresta.proxima
        return [arestas]
    
    def facesDeUmaFace(self, face):
        primeiraAresta = face.aresta
        aresta = None
        faces = []
        while aresta is not primeiraAresta:
            if aresta == None:
                aresta = primeiraAresta
            if aresta.gemea.faceIncidente != None:
                faces.append(aresta.gemea.faceIncidente)
            aresta = aresta.proxima
        return faces
                
def main():
    mesh = Mesh()
    mesh.abrirOBJ(r"C:\Users\RianA\Desktop\Computação Gráfica\Atividade3\Cube.obj")
    mesh.printar()
    mesh.cicloExterno()
    print("\n\n\n")
    print(f'{mesh}')
    while True:
        perguntas(mesh)
    
    
def perguntas(Mesh):
    print(f'Escolha Sua Pergunta: 1-Faces De Um Vertice, 2-Arestas De Um Vertice, 3-Faces De Uma Arestas, 4- Arestas De Uma Face, 5- Faces De Uma Face')
    while True:
        escolha = input("Digite o número correspondente à sua escolha: ")
        try:
            escolha = int(escolha)
            if 1 <= escolha <= 5: 
                break
            else:
                print("Por favor, escolha um número entre 1 e 5.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")
    match escolha:
        case 1:
            print("Você escolheu: Faces De Um Vertice.")
            while True:
                vertice = input('Entre com o Vertice: ')
                try:
                    vertice = int(vertice)
                    if 1 <= vertice <= len(Mesh.vertices):
                        break
                    else:
                        print(f"Por favor, escolha um número entre 1 e {len(Mesh.vertices)}")
                except ValueError:
                    print("Entrada inválida. Por favor, digite um número")
            print(f'Resposta: {Mesh.facesDeUmVertice(Mesh.vertices[vertice-1])}')
        case 2:
            print("Você escolheu: Arestas De Um Vertice.")
            while True:
                vertice = input('Entre com o Vertice: ')
                try:
                    vertice = int(vertice)
                    if 1 <= vertice <= len(Mesh.vertices):
                        break
                    else:
                        print(f"Por favor, escolha um número entre 1 e {len(Mesh.vertices)}")
                except ValueError:
                    print("Entrada inválida. Por favor, digite um número")
            print(f'Resposta: {Mesh.arestasDeUmVertice(Mesh.vertices[vertice-1])}')
        case 3:
            print("Você escolheu: Faces De Uma Aresta.")
            while True:
                aresta = input('Entre com a Aresta: ')
                try:
                    aresta = int(aresta)
                    if 1 <= aresta <= len(Mesh.arestas):
                        break
                    else:
                        print(f"Por favor, escolha um número entre 1 e {len(Mesh.arestas)}")
                except ValueError:
                    print("Entrada inválida. Por favor, digite um número")
            print(f'Resposta: {Mesh.facesDeUmaAresta(Mesh.arestas[aresta-1])}')
        case 4:
            print("Você escolheu: Arestas De Uma Face.")
            while True:
                face = input('Entre com a Face: ')
                try:
                    face = int(face)
                    if 1 <= face <= len(Mesh.faces):
                        break
                    else:
                        print(f"Por favor, escolha um número entre 1 e {len(Mesh.faces)}")
                except ValueError:
                    print("Entrada inválida. Por favor, digite um número")
            print(f'Resposta: {Mesh.arestasDeUmaFace(Mesh.faces[face-1])}')
        case 5:
            print("Você escolheu: Faces De Uma Face.")
            while True:
                face = input('Entre com a Face: ')
                try:
                    face = int(face)
                    if 1 <= face <= len(Mesh.faces):
                        break
                    else:
                        print(f"Por favor, escolha um número entre 1 e {len(Mesh.faces)}")
                except ValueError:
                    print("Entrada inválida. Por favor, digite um número")
            print(f'Resposta: {Mesh.facesDeUmaFace(Mesh.faces[face-1])}')

if __name__ == "__main__":
    main()