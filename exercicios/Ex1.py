class SuffixTree:

    def __init__(self):
        self.nodes = {0: (-1, {})}  # root node
        self.num = 0
        self.seq = ''

    def print_tree(self):
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0:
                print(k, "->", self.nodes[k][1])
            else:
                print(k, ":", self.nodes[k][0])

    def add_node(self, origin, symbol, leafnum=-1):
        self.num += 1  # incrementa o numero do node
        self.nodes[origin][1][symbol] = self.num  # (1 é para ir buscar o dicionario dentro do tuplo)
        self.nodes[self.num] = (leafnum, {})  # constroi o tuplo para o proximo node

    def add_suffix(self, p, sufnum):  # padrao e posicao de inicio do padrao
        pos = 0
        node = 0
        while pos < len(p):
            if p[pos] not in self.nodes[node][1].keys():  # se o nucleotido na posicao pos da seq p nao estiver no node
                if pos == len(p) - 1:  # e se a posicao (pos) estiver na ultima posicao do padrao
                    self.add_node(node, p[pos], sufnum)  # adiciona o node final (folha)
                else:
                    self.add_node(node, p[pos])  # adiciona o node
            node = self.nodes[node][1][p[pos]]  # muda o node para a posicao atual aka o node atual
            pos += 1  # avanca uma posicao

    def suffix_tree_from_seq(self, text):
        self.seq = text
        seq = text + "$"  # adiciona o simbolo no final da string
        for i in range(len(seq)):  # itera pelo tamanho da string t
            self.add_suffix(seq[i:], i)  # passa a seq da posicao i ate ao fim da string, e em que posicao foi iniciada

    def find_pattern(self, pattern):
        pos = 0  # inutil
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():  # se a letra estiver nas keys do dicionario
                node = self.nodes[node][1][pattern[pos]]  # node passa ao value da key
            else:  # caso nao exista no dicionaro
                return None
        return self.get_leaves_below(node)  # acabando de percorrer o pattern

    def get_leaves_below(self, node):
        res = []
        if self.nodes[node][0] >= 0:  # >=0 é o mesmo que !=-1, o que significa que estamos a verificar se é uma folha
            res.append(self.nodes[node][0])  # adiciona o node da folha
        else:
            for k in self.nodes[node][1].keys():  # itera as keys do dicionaro do tuplo
                newnode = self.nodes[node][1][k]  # guarda na variavel o node do da key iterada
                leaves = self.get_leaves_below(
                    newnode)  # recorre a mesma funcao (recursividade) até chegarmo a uma folha
                res.extend(leaves)  # vai concatenar uma lista à lista res
        return res  # retorna

    # ex1a
    def nodes_below(self, node):
        if node not in self.nodes.keys():  # verificar se o argumento dado está presente na arvore
            return 'Nó não existe na árvore'
        else:
            res = []
            for letra in self.nodes[node][1].keys():  # itera as keys do dicionario do no
                res.append(self.nodes[node][1][letra])  # adiciona o value de cada key iterada
            for i in res:  # itera os valores da lista res
                res.extend(self.nodes[i][1].values())  # extende a lista res com os values do dicionaro dos nodes iterados
            return res  # devolve os nodes da arvore abaixo do argumento

    # ex1b
    def matches_prefix(self, prefix):
        if self.find_pattern(prefix) is None: #verificar se o preixo existe
            return 'Não existe esse prefixo'
        else:
            res = []
            pat = self.find_pattern(prefix) #guarda os nodes do padrao na variavel
            seq = self.seq #usa a sequencia original
            for i in pat: #itera os nodes de pat
                hipo = len(seq) - i #numero de hipoteses/seq/padroes possiveis
                tam = len(prefix) #variavel para armazenar o tamanho atual da hipotese; começa com o tamanho do prefixo porque começa sempre com o prefixo
                while tam <= hipo:
                    res.append(seq[i:i + tam]) #adiciona a lista res o excerto da seq entre o valor iterado (i) e i+tam
                    tam += 1 #incrementacao da varivavel tam de modo a quebrar o loop
        return res


def test():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    st.print_tree()
    print(st.find_pattern("TA"))
    print(st.find_pattern("ACG"))
    # testes exercicios
    print('#' * 40)
    print('Exercício 1a:')
    print(st.nodes_below(7))
    print('#' * 40)
    print('Exercício 1b:')
    print(st.matches_prefix('TA'))
    print('#' * 40)


def test2():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    print(st.find_pattern("TA"))
    print(st.repeats(2, 2))


test()
# test2()




# def get_sequence(self):
#     sequence = ''
#     m = self.nodes[0][1].keys()
#     for i in m:
#         if self.nodes[0][1][i] == 1:
#             node = self.nodes[0][1][i]
#             sequence += i
#     p = 1
#     while p != 0:
#         m = self.nodes[node][1].keys()
#         for letra in m:
#             dic = self.nodes[node][1]
#             if dic.get(letra) == node + 1:
#                 node = self.nodes[node][1][letra]
#                 sequence += letra
#                 if self.nodes[node][0] != -1:
#                     p = 0
#     sequence = sequence.strip('$')  # basico
#     return sequence