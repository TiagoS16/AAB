class MyGraph_Custos:

    def __init__(self, g= {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print(v, " -> ", self.graph[v])

    ## get basic info

    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())

    def get_edges(self):
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():
            for des in self.graph[v]:
                d, wg = des
                edges.append((v, d, wg))
        return edges

    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())

    ## add nodes and edges

    def add_vertex(self, v):
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():
            self.graph[v] = []

    def add_edge(self, o, d, wg):
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph '''
        if o not in self.graph.keys():  # verifica se ha o vertice o senao adiciona ao dicionario
            self.add_vertex(o)
        if d not in self.graph.keys():  # verifica se ha d vertice o senao adiciona ao dicionario
            self.add_vertex(d)
        des = []
        for j in self.graph[o]:
            vertice, custo = j #separa o tuplo com o vertice e o custo
            des.append(vertice)
        if d not in des:
            # verifica se ha ligação entre os dois vertices, caso contrario adiciona o vertice d à lista do vertice o
            self.graph[o].append((d, wg))

    ## successors, predecessors, adjacent nodes

    def get_successors(self, v):
        res = []
        for i in self.graph[v]:
            vertice, custo = i
            res.append(vertice)
        return res  # needed to avoid list being overwritten of result of the function is used

    def get_predecessors(self, v):
        res = []
        for i in self.graph.keys():
            for j in self.graph[i]:
                vertice, custo = j
                if vertice == v:
                    res.append(i)
        return res

    def get_adjacents(self, v):
        suc = self.get_successors(v)  # buscar os sucessores
        pred = self.get_predecessors(v)  # buscar os predecessores
        res = pred
        for i in suc:  # adcionar os sucessores não presentes na lista
            if i not in res:
                res.append(i)
        return res

    ## degrees

    def out_degree(self, v):
        return len(self.get_successors(v))

    def in_degree(self, v):
        return len(self.get_predecessors(v))

    def degree(self, v):
        return len(self.get_adjacents(v))

    ## BFS and DFS searches

    def reachable_bfs(self, v):
        l = [v]  # sitio onde tou a começar, lista de coisas a começar, ou seja começa pelo no de origem
        res = []  # a lista do resultado de nos atingiveis
        while len(l) > 0:  # enquanto ha elementos na lista l (lista de queue)
            node = l.pop(0)  # isolar o 1º no na queue
            if node != v:  # se o v não entra na lista de nos acessiveis e for diferente é adiciona a lista
                res.append(node)  # controi o resultado sempre a colocar no fim, ou seja os primeiros ficam para ultimo
            for elem in self.graph[node]:  # correr os nos no node a pesquisar
                vertice, custo = elem
                if vertice not in res and vertice not in l and vertice != node:  # adicionar á queue
                    l.append(vertice)
        return res

    def reachable_dfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v:  # se o v não entra na lista de nos acessiveis e for diferente é adiciona a lista
                res.append(node)  # controi o resultado sempre a colocar no fim, ou seja os primeiros ficam para ultimo
            s = 0
            for elem in self.graph[node]:
                vertice, custo = elem
                if vertice not in res and vertice not in l:
                    l.insert(s, vertice)
                    s += 1
        return res

    def distance(self, s, d):
        if s == d:
            return 0
        else:
            l = [(s, 0)]  # sitio onde tou a começar, lista de coisas a começar, ou seja começa pelo no de origem
            visited = [s]  # a lista do resultado de nos atingiveis
            while len(l) > 0:  # enquanto ha elementos na lista l (lista de queue)
                node, dist = l.pop(0)  # isolar o 1º no na queue (dist é o custo acumulado)
                for elem in self.graph[node]:  # correr os nos no node a pesquisar
                    vertice, custo = elem
                    if vertice == d:
                        return dist + custo
                    if vertice not in visited:
                        l.append((vertice, dist + custo)) #adicionar à queue
                        visited.append(vertice)
            return None

    def shortest_path(self, s, d):  #algoritmo de dijkstra
        if s == d:
            return [s, d]
        else:
            l = [(s, [], 0)]  # sitio onde tou a começar, lista de coisas a começar, ou seja começa pelo no de origem
            visited = [s]  # a lista do resultado de nos atingiveis
            while len(l) > 0:  # enquanto ha elementos na lista l (lista de queue)
                node, path, dist = l.pop(0)  # isolar o 1º no na queue
                custo_min = 999999999
                for elem in self.graph[node]:  # correr os nos no node a pesquisar
                    vertice, custo = elem
                    if vertice == d:
                        return path + [(node, vertice)], dist + custo
                    if custo < custo_min:
                        custo_min = custo
                        vert_custo_min = vertice #altera o vertice para o vertice com o custo minimo
                if vert_custo_min not in visited and vert_custo_min not in l and vert_custo_min != node:  # adicionar á queue
                    l.append((vert_custo_min, path + [(node, vert_custo_min)], dist + custo_min))
                    visited.append(vert_custo_min)
            return None

    def reachable_with_dist(self,s):  # travessia total do grafo mas com as distancias associadas, faz a travessia sobre todos os pontos
        res = []
        l = [(s, 0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s:
                res.append((node, dist))
            for elem in self.graph[node]:
                vertice, custo = elem
                if not is_in_tuple_list(l, vertice) and not is_in_tuple_list(res, vertice):  # juntar sempre a distancia ao registro dos elementos nos grafos
                    l.append((vertice, dist + custo))
        return res

    ## cycles
    def node_has_cycle(self, v):
        l = [v]
        #res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                vertice, custo = elem
                if vertice == v:
                    return True
                elif vertice not in visited:
                    l.append(vertice)
                    visited.append(vertice)
        return False #res

    def has_cycle(self):
        #res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v):
                return True
        return False #res


def is_in_tuple_list(tl, val):
    #res = False
    for (x, y) in tl:
        if val == x:
            return True
    return False #res


def test1():
    #gr = MyGraph_Custos({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})  # criar o grafo
    grafo = MyGraph_Custos({1: [(2, 2)], 2: [(3, 4), (4, 3)], 3: [(5, 1)], 4: [(5, 3), (6, 5)], 5: [], 6: []})
    grafo.print_graph()
    print('#' * 40)
    print(grafo.get_nodes())
    print('#' * 40)
    print(grafo.get_edges())
    print('#' * 40)


def test2():
    gr2 = MyGraph_Custos()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)

    gr2.add_edge(1, 2, 2)
    gr2.add_edge(2, 3, 4)
    gr2.add_edge(2, 4, 3)
    gr2.add_edge(3, 5, 1)
    gr2.add_edge(4, 5, 3)
    gr2.add_edge(4, 6, 5)

    gr2.print_graph()


def test3():
    #gr = MyGraph_Custos({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})
    grafo = MyGraph_Custos({1: [(2, 2)], 2: [(3, 4), (4, 3)], 3: [(5, 1)], 4: [(5, 3), (6, 5)], 5: [], 6: []})
    grafo.print_graph()
    print('#' * 40)
    print(grafo.get_successors(2))
    print('#' * 40)
    print(grafo.get_predecessors(2))
    print('#' * 40)
    print(grafo.get_adjacents(2))
    print('#' * 40)
    print(grafo.in_degree(2))
    print('#' * 40)
    print(grafo.out_degree(2))
    print('#' * 40)
    print(grafo.degree(2))
    print('#' * 40)


def test4():
    #gr = MyGraph_Custos({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})
    grafo = MyGraph_Custos({1: [(2, 2)], 2: [(3, 4), (4, 3)], 3: [(5, 1)], 4: [(5, 3), (6, 5)], 5: [], 6: []})

    print('#' * 40)
    print(grafo.distance(1, 5))
    print('#' * 40)
    print(grafo.distance(2, 6))
    print('#' * 40)

    print(grafo.shortest_path(1, 5))
    print('#' * 40)
    print(grafo.shortest_path(2, 6))
    print('#' * 40)

    print(grafo.reachable_with_dist(1))
    print('#' * 40)
    print(grafo.reachable_with_dist(2))
    print('#' * 40)

    gr2 = MyGraph_Custos({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})

    print('#' * 40)
    print(gr2.distance(2, 1))
    print('#' * 40)
    print(gr2.distance(1, 4))
    print('#' * 40)

    print(gr2.shortest_path(1, 5))
    print('#' * 40)
    print(gr2.shortest_path(2, 4))
    print('#' * 40)

    print(gr2.reachable_with_dist(1))
    print('#' * 40)
    print(gr2.reachable_with_dist(4))
    print('#' * 40)


def test5():
    gr = MyGraph_Custos({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})
    #grafo = MyGraph_Custos({1: [(2, 2)], 2: [(3, 4), (4, 3)], 3: [(5, 1)], 4: [(5, 3), (6, 5)], 5: [], 6: []})

    print('#' * 40)
    print(gr.node_has_cycle(2))
    print('#' * 40)
    print(gr.node_has_cycle(1))
    print('#' * 40)
    print(gr.has_cycle())
    print('#' * 40)

    #gr2 = MyGraph_Custos({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})
    #print(gr2.node_has_cycle(1))
    #print(gr2.has_cycle())


if __name__ == "__main__":
    #test1()
    test2()
    #test3()
    #test4()
    #test5()
