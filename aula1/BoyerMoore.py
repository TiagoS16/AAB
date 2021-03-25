
class BoyerMoore:
    
    def __init__(self, alphabet, pattern):
        self.alphabet = alphabet
        self.pattern = pattern
        self.preprocess()

    def preprocess(self):
        self.process_bcr()
        self.process_gsr()
        
    def process_bcr(self):
        '''Implementação do Bad Caracter Rule'''
        self.occ = {} #abre um dicionario
        for c in self.alphabet: #adiciona ao dicionario todas as letras do alfabeto com o valor -1
            self.occ[c] = -1
        for i in range(len(self.pattern)): #altera no dicionario a letra do padrao para o valor do iterador
            self.occ[self.pattern[i]] = i

            
    def process_gsr(self):
        '''Implementação do Good Suffix Rule'''
        self.f = [0] * (len(self.pattern) + 1) #abre uma lista com o numero de zeros igual ao comprimento do padrao
        self.s = [0] * (len(self.pattern) + 1)
        i = len(self.pattern) #define i como o comprimento do padrao
        j = i + 1 #define i como o comprimento do padrao + 1
        self.f[i] = j #muda o ultimo elemento da lista f para j
        while i > 0:
            while j <= len(self.pattern) and self.pattern[i-1] != self.pattern[j-1]: #enquanto j for <= ao comprimento do padrao e a letra do padrao na posicao i-1 for diferente da letra na posicao j-1
                if self.s[j] == 0:
                    self.s[j] = j - i #a posicao de j vai tomar o valor de j - i
                j = self.f[j] #j vai ficar a posicao de self.f[j]
            i -= 1
            j -= 1
            self.f[i] = j
        j = self.f[0]
        for i in range(len(self.pattern)):#quando o valor é 0, altera para o valor de j mais recente que significa passar o restaste da cadeia
            if self.s[i] == 0:
                self.s[i] = j #a posicao de i em self.s sera o ultimo valor de j
            if i == j:
                self.f[j]

        
        
    def search_pattern(self, text):
        print(self.s)
        print(self.f)
        res = []
        i = 0
        while i <= (len(text) - len(self.pattern)):
            j = len(self.pattern) - 1
            while j >= 0 and self.pattern[j] == text[j+i]:
                j -= 1
            if j < 0:
                res.append(i)
                i = i + self.s[0] #avança i para
            else:
                c = text[j+i]
                i += max(self.s[j+1], j-self.occ[c]) #avancar na seq dependendo da GSR and BCR
        return res

def wtest():
    bm = BoyerMoore("ACTG", "AACC")
    print (bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC"))

wtest()

# result: [5, 13, 23, 37]