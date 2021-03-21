class SuffixTree_ex2:

    def __init__(self):
        self.nodes = {0: (-1, {})}  # root node
        self.num = 0
        self.seq1 = ''
        self.seq2 = ''

    def unzip(self, k):
        if self.nodes[k][0] == -1:
            m = self.nodes[k][0]
            n = ''
        else:
            m, n = self.nodes[k][0]
        return m, n

    def print_tree(self):
        for k in self.nodes.keys():
            m, n = self.unzip(k)
            if m < 0:
                print(k, "->", self.nodes[k][1])
            else:
                print(k, ":", m, n)

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

    def suffix_tree_from_seq(self, seq1, seq2):
        s1 = seq1 + "$"  # adiciona o simbolo no final da string
        s2 = seq2 + '#'
        self.seq1 = seq1
        self.seq2 = seq2
        for i in range(len(s1)):  # itera pelo tamanho da string t
            self.add_suffix(s1[i:], (0, i))  # passa a seq da posicao i ate ao fim da string, e em que posicao foi iniciada
        for j in range(len(s2)):
            self.add_suffix(s2[j:], (1, j))


    def find_pattern(self, pattern):
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():  # se a letra estiver nas keys do dicionario
                node = self.nodes[node][1][pattern[pos]]  # node passa ao value da key
            else:  # caso nao exista no dicionaro
                return None
        return self.get_leaves_below(node)  # acabando de percorrer o pattern, passa o nde para a funcao

    def get_leaves_below(self, node):
        res1 = []
        res2 = []
        m, n = self.unzip(node)
        if m >= 0:  # >=0 é o mesmo que !=-1, o que significa que estamos a verificar se é uma folha
            if m == 1:
                res1.append(n) # adiciona o node da folha
            else:
                res2.append(n)
        else:
            for k in self.nodes[node][1].keys():  # itera as keys do dicionaro do tuplo
                newnode = self.nodes[node][1][k]  # guarda na variavel o node do da key iterada
                leaves1, leaves2 = self.get_leaves_below(newnode)  # recorre a mesma funcao (recursividade) até chegarmo a uma folha
                res1.extend(leaves1)  # vai concatenar uma lista à lista res
                res2.extend(leaves2)
        return (res1, res2)


    def largestCommonSubstring(self):
        seq1 = self.seq1
        seq2 = self.seq2
        match = ''
        for i in range(0, len(seq1)):
            for j in range(0, len(seq2)):
                k = 1
                # loop so acontece quando o i+k e j+k sao <= ao tamanho das suas seqs e quando o mesmo splice nas duas seqs sao iguais
                while i + k <= len(seq1) and j + k <= len(seq2) and seq1[i:i + k] == seq2[j:j + k]:
                    if len(match) <= len(seq1[i:i + k]): #guarda o splice da seq1 na match enquanto o tamanho da mesma for <= ao tamanho do splice
                        match = seq1[i:i + k]
                    k += 1
        return match


def test():
    seq1 = "TACTA"
    seq2 = "TATAC"
    st = SuffixTree_ex2()
    st.suffix_tree_from_seq(seq1, seq2)
    st.print_tree()
    print('#' * 40)
    print(st.find_pattern("TA"))
    print('#' * 40)
    print(st.largestCommonSubstring())
    print('#' * 40)

test()


