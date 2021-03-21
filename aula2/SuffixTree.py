
class SuffixTree:
    
    def __init__(self):
        self.nodes = { 0:(-1,{}) } # root node
        self.num = 0
    
    def print_tree(self):
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0:
                print (k, "->", self.nodes[k][1]) 
            else:
                print (k, ":", self.nodes[k][0])
                
    def add_node(self, origin, symbol, leafnum = -1):
        self.num += 1 #incrementa o numero do node
        self.nodes[origin][1][symbol] = self.num #(1 é para ir buscar o dicionario dentro do tuplo)
        self.nodes[self.num] = (leafnum,{}) #constroi o tuplo para o proximo node
        
    def add_suffix(self, p, sufnum): #padrao e posicao de inicio do padrao
        pos = 0
        node = 0
        while pos < len(p):
            if p[pos] not in self.nodes[node][1].keys(): #se o nucleotido na posicao pos da seq p nao estiver no node
                if pos == len(p) - 1: #e se a posicao (pos) estiver na ultima posicao do padrao
                    self.add_node(node, p[pos], sufnum) #adiciona o node final (folha)
                else:
                    self.add_node(node, p[pos]) #adiciona o node
            node = self.nodes[node][1][p[pos]] #muda o node para a posicao atual aka o node atual
            pos += 1 #avanca uma posicao
    
    def suffix_tree_from_seq(self, text):
        t = text + "$" #adiciona o simbolo no final da string
        for i in range(len(t)): #itera pelo tamanho da string t
            self.add_suffix(t[i:], i) #passa a seq da posicao i ate ao fim da string, e em que posicao foi iniciada
            
    def find_pattern(self, pattern):
        pos = 0 #inutil
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys(): #se a letra estiver nas keys do dicionario
                node = self.nodes[node][1][pattern[pos]] #node passa ao value da key
            else: #caso nao exista no dicionaro
                return None
        return self.get_leaves_below(node) #acabando de percorrer o pattern
        

    def get_leaves_below(self, node):
        res = []
        if self.nodes[node][0] >= 0: # >=0 é o mesmo que !=-1, o que significa que estamos a verificar se é uma folha
            res.append(self.nodes[node][0]) #adiciona o node da folha
        else:
            for k in self.nodes[node][1].keys(): #itera as keys do dicionaro do tuplo
                newnode = self.nodes[node][1][k] #guarda na variavel o node do da key iterada
                leaves = self.get_leaves_below(newnode) #recorre a mesma funcao (recursividade) até chegarmo a uma folha
                res.extend(leaves) #vai concatenar uma lista à lista res
        return res #retorna


def test():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    st.print_tree()
    print (st.find_pattern("TA"))
    print (st.find_pattern("ACG"))


def test2():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    print (st.find_pattern("TA"))
    print(st.repeats(2,2))

test()
print()
test2()
        
