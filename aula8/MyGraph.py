## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:
    
    def __init__(self, g= {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g    

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print (v, " -> ", self.graph[v])

    ## get basic info

    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())
        
    def get_edges(self): 
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys(): #percorrer todas as keys
            for d in self.graph[v]: #percorrer todos os values
                edges.append((v,d))
        return edges
      
    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())
      
    ## add nodes and edges

    def add_vertex(self, v): #feito na aula
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.get_nodes():
            self.graph[v] = []
        
    def add_edge(self, o, d): #feito na aula
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph '''
        if o not in self.get_nodes():
            self.add_vertex(o)
        if d not in self.get_nodes():
            self.add_vertex(d)
        if d not in self.graph[o]:
            self.graph[o].append(d)

    ## successors, predecessors, adjacent nodes
        
    def get_successors(self, v):
        return list(self.graph[v])     # needed to avoid list being overwritten of result of the function is used
             
    def get_predecessors(self, v): #feito na aula
        res= []
        for i in self.graph.keys():
            if v in self.graph[i]:
                res.append(i)
        return res

    def get_adjacents(self, v): #feito na aula
        suc= self.get_successors(v)
        pred= self.get_predecessors(v)
        res= pred
        for i in suc:
            if i not in res:
                res.append(i)
        return res


    ## degrees
    
    def out_degree(self, v): #feito na aula
        return len(self.get_successors(v))

    def in_degree(self, v): #feito na aula
        return len(self.get_predecessors(v))

    def degree(self, v): #feito na aula
        return len(self.get_adjacents(v))
    
    ## BFS and DFS searches
    
    def reachable_bfs(self, v): #em largura
        l = [v] #nos que ainda tem de ser processados; quando vazia acabou a pesquisa
        res = [] #nos atingiveis/o que já foi visitado
        while len(l) > 0: # enquanto ha elementos na lista l (lista de queue)
            node = l.pop(0) # isolar o primeiro elemento da lista de queue
            if node != v: #se o node for diferente de v vai adicionar o node a res
                res.append(node)
            for elem in self.graph[node]: #para todos os sucessores do node
                if elem not in res and elem not in l and elem != node: #verifica que nao existe em res e em l e verifica se o sucessor é diferente do node
                    l.append(elem) #adicionar a queue para verificar mais tarde
        return res
        
    def reachable_dfs(self, v): #em profundidade
        l = [v]
        res = []
        while len(l) > 0: #enquanto ha elementos na lista l (lista de queue)
            node = l.pop(0) #isolar o primeiro elemento da lista de queue
            if node != v:
                res.append(node)
            s = 0 #ira ser usado para criar o stack//é reposto a 0 antes do loop for abaixo
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem) #cria um stack/vai voltar a verificar o mais recente/insere no inicio da lista
                    s += 1 #caso haja multiplos sucessores, o s vai aumentar de forma a colocar as proximas iteraçoes na posicao depois da iteraçao anterior (stack)
        return res    
    
    def distance(self, s, d): #feito na aula
        if s == d:
            return 0
        else:
            l = [(s, 0)] #lista com os tuplos do no e a distancia
            visited = [s] #nos visitados
            while len(l) > 0: #enquanto ha elementos na lista l (lista de queue)
                node, dist = l.pop(0)
                for elem in self.graph[node]:
                    if elem == d:
                        return dist + 1
                    elif elem not in visited:
                        l.append((elem, dist + 1)) #queue
                        visited.append(elem)
            return None
        
    def shortest_path(self, s, d): #feito na aula
        if s == d:
            return [s, d]
        else:
            l = [(s, [])] #lista com com um tuplo com o no e o caminho ate la
            visited = [s] #nos visitados
            while len(l) > 0:
                node, path = l.pop(0)
                for elem in self.graph[node]: #itera os sucessores do node
                    if elem == d:
                        return path + [node, d] #chegando ao destino retorna a lista com o caminho
                    elif elem not in visited:
                        l.append((elem, path + [node]))
                        visited.append(elem)
        return None
        
    def reachable_with_dist(self, s): #travessia total do grafo mas com as distancias associadas, faz a travessia sobre todos os pontos
        res = []
        l = [(s,0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s:
                res.append((node, dist))
            for elem in self.graph[node]:
                if not is_in_tuple_list(l, elem) and not is_in_tuple_list(res, elem): #juntar sempre a distancia ao registro dos elementos nos grafos
                    l.append((elem, dist + 1))
        return res

## cycles
    def node_has_cycle(self, v):
        l = [v]
        #res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v:
                    return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
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
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()
    print (gr.get_nodes())
    print (gr.get_edges())
    

def test2():
    gr2 = MyGraph()
    #gr2.add_vertex(1)
    #gr2.add_vertex(2)
    #gr2.add_vertex(3)
    #gr2.add_vertex(4)
    
    gr2.add_edge(1,2)
    gr2.add_edge(2,3)
    gr2.add_edge(3,2)
    gr2.add_edge(3,4)
    gr2.add_edge(4,2)
    
    gr2.print_graph()
  
def test3():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()

    print (gr.get_successors(2))
    print('#'*40)
    print (gr.get_predecessors(2))
    print('#' * 40)
    print (gr.get_adjacents(2))
    print('#' * 40)
    print (gr.in_degree(2))
    print('#' * 40)
    print (gr.out_degree(2))
    print('#' * 40)
    print (gr.degree(2))
    print('#' * 40)

def test4():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    
    print (gr.distance(1,4))
    print('#' * 40)
    print (gr.distance(4,3))
    print('#' * 40)

    print (gr.shortest_path(1,4))
    print('#' * 40)
    print (gr.shortest_path(4,3))
    print('#' * 40)

    print (gr.reachable_with_dist(1))
    print('#' * 40)
    print (gr.reachable_with_dist(3))
    print('#' * 40)

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    
    print (gr2.distance(2,1))
    print('#' * 40)
    print (gr2.distance(1,5))
    print('#' * 40)

    print (gr2.shortest_path(1,5))
    print('#' * 40)
    print (gr2.shortest_path(2,1))
    print('#' * 40)

    print (gr2.reachable_with_dist(1))
    print('#' * 40)
    print (gr2.reachable_with_dist(5))
    print('#' * 40)

def test5():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    print (gr.node_has_cycle(2))
    print('#' * 40)
    print (gr.node_has_cycle(1))
    print('#' * 40)
    print (gr.has_cycle())
    print('#' * 40)

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    print (gr2. node_has_cycle(1))
    print('#' * 40)
    print (gr2.has_cycle())
    print('#' * 40)


if __name__ == "__main__":
    #test1()
    #test2()
    #test3()
    test4()
    #test5()
