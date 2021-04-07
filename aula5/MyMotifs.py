# -*- coding: utf-8 -*-
"""
@author: miguelrocha
"""

def createMatZeros (nl, nc): #função que vai criar uma matriz de 0, com o temanho de nl * nc dependendo dos valores dados nestas variáveis 
    res = [ ] 
    for i in range(0, nl):
        res.append([0]*nc)
    return res

def printMat(mat): #função responsável por dar print a matriz, neste caso vai dar print lista a lista dentro da matriz
    for i in range(0, len(mat)): print(mat[i])

class MyMotifs:

    def __init__(self, seqs): #calsse recebe sempre uma lista de seq
        self.size = len(seqs[0]) #comprimentos de caractares das seq
        self.seqs = seqs # objetos classe MySeq/ vai ser a nossa lista de seqs
        self.alphabet = seqs[0].alfabeto() #vai a classe myseq chamar a função alfabeto, para dar return de um tipo de alfabeto
        self.doCounts() #criar a matriz de contagens das letras entre as seqs
        self.createPWM() #criar a matriz de PWM, que é a matriz de probabilidades
        
    def __len__ (self): #return do comprimento das seqs
        return self.size       
        
    def doCounts(self): #cria as matrizes de contagens
        self.counts = createMatZeros(len(self.alphabet), self.size)
        for s in self.seqs:
            for i in range(self.size):
                lin = self.alphabet.index(s[i])
                self.counts[lin][i] += 1
                
    def createPWM(self): #cria a mtriz de probabilidades
        if self.counts == None: self.doCounts()
        self.pwm = createMatZeros(len(self.alphabet), self.size)
        for i in range(len(self.alphabet)):
            for j in range(self.size):
                self.pwm[i][j] = float(self.counts[i][j]) / len(self.seqs)
                
    def consensus(self): #vai procurar o consensus na matriz dos counts por coluna
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet) ):
                if self.counts[i][j] > maxcol: 
                    maxcol = self.counts[i][j]
                    maxcoli = i
            res += self.alphabet[maxcoli]        
        return res

    def maskedConsensus(self): #vai procurar o masked consensus que é a consensus mas só com as letras que tem uma incidência maior do que 50% em todas as seqs
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet) ):
                if self.counts[i][j] > maxcol: 
                    maxcol = self.counts[i][j]
                    maxcoli = i
            if maxcol > len(self.seqs) / 2:
                res += self.alphabet[maxcoli]        
            else:
                res += "-"
        return res

    def probabSeq (self, seq): #vai calcular a probabilidade de a seq fazer parte deste quadro
        res = 1.0
        for i in range(self.size):
            lin = self.alphabet.index(seq[i])
            res *= self.pwm[lin][i]
        return res
    
    def probAllPositions(self, seq): #este em vez de calcular a probabilidade de acontecer devolve uma lista com as probabilidades de acontecer em cada letra da seq
        res = []
        for k in range(len(seq)-self.size+1):
            res.append(self.probabSeq(seq))
        return res

    def mostProbableSeq(self, seq): #vai ver qual a posição inicial da subseq de uma seq de comprimento indefenido encaixa melhor no quandro de motifs das seqs
        maximo = -1.0
        maxind = -1
        for k in range(len(seq)-self.size):
            p = self.probabSeq(seq[k:k+ self.size])
            if(p > maximo):
                maximo = p
                maxind = k
        return maxind

def test():
    # test
    from MySeq import MySeq
    seq1 = MySeq("AAAGTT")
    seq2 = MySeq("CACGTG")
    seq3 = MySeq("TTGGGT")
    seq4 = MySeq("GACCGT")
    seq5 = MySeq("AACCAT")
    seq6 = MySeq("AACCCT")
    seq7 = MySeq("AAACCT")
    seq8 = MySeq("GAACCT")
    lseqs = [seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8]
    motifs = MyMotifs(lseqs)
    printMat (motifs.counts)
    printMat (motifs.pwm)
    print(motifs.alphabet)
    
    print(motifs.probabSeq("AAACCT"))
    print(motifs.probabSeq("ATACAG"))
    print(motifs.mostProbableSeq("CTATAAACCTTACATC"))
    
    print(motifs.consensus())
    print(motifs.maskedConsensus())

if __name__ == '__main__':
    test()
