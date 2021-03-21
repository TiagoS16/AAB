# -*- coding: utf-8 -*-

class Trie:
    
    def __init__(self):
        self.nodes = { 0:{} } # dictionary
        self.num = 0
    
    def print_trie(self):
        for k in self.nodes.keys():
            print (k, "->" , self.nodes[k]) 
    
    def add_node(self, origin, symbol):
        # contador do numero de nos
        self.num += 1
        #indexa ao dicionario
        self.nodes[origin][symbol] = self.num
        #cria um novo node (key) com um dicionario vazio (value)
        self.nodes[self.num] = {}
    
    def add_pattern(self, p):
        pos = 0
        node = 0
        #enquanto a posicao for menor que o tamanho do padrao
        while pos < len(p):
            #p[pos] corresponde  a uma base ATCG/verifica se a letra ja esta presente no node
            if p[pos] not in self.nodes[node].keys():
                #adiciona a letra ao node da arvore
                self.add_node(node, p[pos])
            #define o novo node como o node onde estamos
            node = self.nodes[node][p[pos]]
            #passa para a proxima posicao
            pos += 1
            
    def trie_from_patterns(self, pats):
        #itera uma lista de padroes
        for p in pats:
            self.add_pattern(p)
            
    def prefix_trie_match(self, text):
        pos = 0
        match = ""
        node = 0
        while pos < len(text):
            if text[pos] in self.nodes[node].keys(): #verifica se o nucleotido esta presente na arvore
                node = self.nodes[node][text[pos]] #guarda o node em que o nucleotido esta na arvore (value do dicionario dentro do dicionario)
                match += text[pos] #adicona o nucleotido ao padrao
                if self.nodes[node] == {}: #atingindo um folha da arvore (um dicionario vazio)
                    return match #retorna o padrao ja existente na arvore
                else: #caso nao atinja uma folha vai incrementar em 1 a posicao e volta ao ciclo
                    pos += 1
            else: #interrompe o ciclo se o nucleotido nao estiver na arvore
                return None
        return None
        
    def trie_matches(self, text):
        res = []
        for i in range(len(text)): #itera cada caracter da string text
            m = self.prefix_trie_match(text[i:]) #fornece como argumento a funcao a string text desde a letra iterada ate ao final da mesma e guarda o resultado na variavel
            if m != None: #caso a varivavel m seja diferente de None
                res.append((i, m)) #adiciona à lista res o tuplo com a posicao iterada e o match encontrado
        return res
        
          
def wtest():
    patterns = ["GAT", "CCT", "GAG"]
    t = Trie()
    t.trie_from_patterns(patterns)
    t.print_trie()

   
def wtest2():
    patterns = ["AGAGAT", "AGC", "AGTCC", "CAGAT", "CCTA", "GAGAT", "GAT", "TC"]
    t = Trie()
    t.trie_from_patterns(patterns)
    print (t.prefix_trie_match("GAGATCCTA"))
    print (t.trie_matches("GAGATCCTA"))
    
wtest()
print()
wtest2()
