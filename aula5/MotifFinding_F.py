# -*- coding: utf-8 -*-

from MySeq import MySeq
from MyMotifs import MyMotifs

class MotifFinding:
    
    def __init__(self, size = 8, seqs = None):
        self.motifSize = size #vai ver qual é o tamanho dos motifs a procurar se n for nenhum escolhido é 8
        if (seqs != None): #se tivermos seqs o self.seqs vai ser seqs e o self.alphabet vai ser o alfabeto
            self.seqs = seqs
            self.alphabet = seqs[0].alfabeto()
        else:
            self.seqs = [] #se for None vamos dizer que o self.seqs vai ser uma lista vazia
                    
    def __len__ (self):
        return len(self.seqs) #dá return ao nûmero de elementos na lista self.seqs 
    
    def __getitem__(self, n):
        return self.seqs[n] #dá return á string da primeira seq em self.seqs
    
    def seqSize (self, i):
        return len(self.seqs[i]) #dá return ao comprimento da sequêndia i na lista self.seqs
    
    def readFile(self, fic, t): #vai ler um ficheiro e adiciona-lo á nossa lista self.seqs, sendo o t o tipo de seq
        for s in open(fic, "r"):
            self.seqs.append(MySeq(s.strip().upper(),t))
        self.alphabet = self.seqs[0].alfabeto()
        
        
    def createMotifFromIndexes(self, indexes): #recebe uma lista de númereos sendo esta composta pelo número onde cada seq vai começar a contar o motif()
        pseqs = []
        for i,ind in enumerate(indexes):
            pseqs.append( MySeq(self.seqs[i][ind:(ind+self.motifSize)], self.seqs[i].tipo) ) #vai adicionar a pseqs (uma sequência i  onde começa o motif e onde vai acabar) mais o tipo de seq que é
        return MyMotifs(pseqs) #vai correr os Mymotifs com a lista de motifs
        
        
    # SCORES
        
    def score(self, s):
        score = 0
        motif = self.createMotifFromIndexes(s)
        motif.doCounts() #vai cirar a matriz de contagens
        mat = motif.counts #vai tranporta le para aqui
        for j in range(len(mat[0])): #vai correr as colunas da matriz
            maxcol = mat[0][j] #vai dizer que o maxcolun vai ser igual ao primeiro elemento da coluna
            for  i in range(1, len(mat)): #depois vai começar no segundo elemento da coluna e vai comparar com todos os elementos da coluna para ver qual é o maior
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score += maxcol #vai adionar esse valor a coluna
        return score
   
    def scoreMult(self, s): #faz o mesmo de cima mas é com probabilidades e o score vem em probabilidade é por multiplicação
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        motif.createPWM()
        mat = motif.pwm
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score *= maxcol
        return score     
       
    # EXHAUSTIVE SEARCH
    def nextSol (self, s):
        nextS = [0]*len(s) #vai criar a lista s com o em toda ela lista que vai conter em que posição das seqs está a começar a formação dos motifs
        pos = len(s) - 1   #pos vai ser igual ao comprimento da lista s -1
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if (pos < 0): 
            nextS = None #quando NextS = None vamos ter a finalização e vamos ter como resultado as posições nas seq onde se encontra os motifs
        else:
            for i in range(pos): #vai igualar a S á next s mais vai incrementar a ultima elemento de s mais 1 
                nextS[i] = s[i]
            nextS[pos] = s[pos]+1
            for i in range(pos+1, len(s)): # vai acrescentar um 0 a lista s se esta não for composta por valores de s
                nextS[i] = 0
        return nextS
        
    def exhaustiveSearch(self):
        melhorScore = -1
        res = []
        s = [0]* len(self.seqs) #vai cirar a lista de 0 com o numero de seqs presentes na lista self.seqs
        while (s!= None):
            sc = self.score(s) #vai calcular o score das posições
            if (sc > melhorScore): #se esse score for maior do que o melhor score o melhor score passa a ser esse e a lista com as posições iniciais dos motifs passam a ser s
                melhorScore = sc
                res = s
            s = self.nextSol(s) # o próximo s vai ser o nexts
        return res #O resultado são as posições inicais que vão maximizar o score
     
    # BRANCH AND BOUND     
     
    def nextVertex (self, s):
        res =  []
        if len(s) < len(self.seqs): # internal node -> down one level #se o comprimento de len(s) for menor implica que n está a abranjer as seqs todas logo ira dar append a mais um 0 e vai dar essa s como o nexts
            for i in range(len(s)): 
                res.append(s[i])
            res.append(0)
        else: # bypass
            pos = len(s)-1 
            while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize: #vai ver se a ultima seq já chegou ao fim e assim sucessivamente
                pos -= 1 
            if pos < 0: res = None # last solution #vai acabar o ciclo, implica que chegou a ultima hipotese
            else:
                for i in range(pos): res.append(s[i]) #vai criar a próxima lista s e vai adicionar ao ultimo valor +1
                res.append(s[pos]+1)
        return res
    
    
    def bypass (self, s): #vai ver se já chegou as ultimas letras de seq, se chegou vai alteralas para 0 e vai acrescentalas
        res =  []
        pos = len(s) -1
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if pos < 0: res = None 
        else:
            for i in range(pos): res.append(s[i])
            res.append(s[pos]+1)
        return res
        
    def branchAndBound (self):
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0]*size #vai criar a mesma lista s
        while s != None: #enquanto o s não for None ele vai sempre continuar
            if len(s) < size: #se o len s for menor implica que n está a abranjer todas as seqs, log vai ao bypass, se o optimscore for mais pequeno que o melhorscore, não vamos incrementar na folha mas sim vamos incrementar nos nódulas dando skip a certas folhas, onde vamos saber que o score vai ser menor
                optimScore = self.score(s) + (size-len(s)) * self.motifSize
                if optimScore < melhorScore: s = self.bypass(s)
                else: s = self.nextVertex(s)
            else:
                sc = self.score(s) #calcular o score dos motifs
                if sc > melhorScore: #se o scor for maior que o mais maior vai alterar o melhor score e o melhorMotif
                    melhorScore = sc
                    melhorMotif  = s
                s = self.nextVertex(s) #e vai fazer que o s seja o Nexts
        return melhorMotif

    # Consensus (heuristic)
  
    def heuristicConsensus(self):
        """ Procura as posições para o motif nas duas primeiras sequências """ 
        mf = MotifFinding(self.motifSize, self.seqs[:2]) #Procura exaustiva das duas primeiras sequências
        s = mf.exhaustiveSearch() #vai procurar a posição inical entre essas 2 seqs com o score ideal
        for a in range(2, len(self.seqs)): #Avalia a melhor posição para cada uma das outras sequências, guardando-a (maximiza o score)
            s.append(0)
            melhorScore = -1 
            melhorPosition = 0
            for b in range(self.seqSize(a) - self.motifSize + 1):
                s[a] = b 
                scoreatual = self.score(s)
                if scoreatual > melhorScore:
                    melhorScore = scoreatual
                    melhorPosition = b
                s[a] = melhorPosition
        return s

    # Consensus (heuristic)

    def heuristicStochastic (self):
        from random import randint
        s = [0] * len(self.seqs) #Gerar um vetor aleatória com o mesmo tamnho do número de sequências
        #Passo 1: inicia todas as posições com valores aleatórios 
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize) #vai escolher um valor random para ser o valor inicial de cada seq
        #Passo 2
        melhorscore = self.score(s)
        improve = True
        while improve:
            motif = self.createMotifFromIndexes(s) #Constrói o perfil com base nas posições iniciais s
            motif.createPWM() #vai criar a matriz PWM  
            #Passo 3
            for i in range(len(self.seqs)): #Avalia a melhor posição inicial para cada sequência com base no perfil
                s[i] = motif.mostProbableSeq(self.seqs[i]) #vai ver em cada seq de self.seqs, qual é a subseq nelas que é mais provável de acontecer no quandro PWM
            #Passo 4
            #Verifica se houve alguma melhoria
            scr = self.score(s) #vai calcular o score
            if scr > melhorscore: #se o score melhorou volta a repetir o processo se não acaba e devolve as melhores posições das subseqs
                melhorscore = scr
            else: 
                improve = False
        return s

    # Gibbs sampling 

    def gibbs (self, iterations = 1000):

        from random import randint
        s = [] #criar a lista s de posições iniciais
        #Passo 1
        for i in range(len(self.seqs)):
             s.append(randint(0, len(self.seqs[i]) - self.motifSize -1)) #escolher um numero random de start para cada sequência
        melhorscore = self.score(s) #calcular o score de s
        bests = list(s)
        for it in range(iterations):
            #Passo 2: selecionar uma das sequência aleatoriamente
            seq_idx = randint(0, len(self.seqs) - 1)
            #Passo 3: criar um perfil que não contenha a sequência aleatória
            seq = self.seqs[seq_idx] #indicar qual a seq que vai remover
            s.pop(seq_idx) #vai remover a posição inicial correspondente a seq escolhida para ser removida
            removed = self.seqs.pop(seq_idx) #vai dar pop sa seq na lista e guardar no removed
            motif = self.createMotifFromIndexes(s) #Criar o perfil sem a sequência removida
            motif.createPWM()
            self.seqs.insert(seq_idx, removed) #vai voltar a adicionar a seq removida a lista de seqs na posição seq_idx
            r = motif.probAllPositions(seq) #vai calcular a probabilidade de todas as subseqs possiveis na seq removida
            pos = self.roulette(r) #vai fazer o roulette da lista e escolher um dos valores com valores maior que 0, devolvendo a posição onde se iniciou o motif
            s.insert(seq_idx, pos) #vai adicionar o valor da pos do motif ao s na posição seq_idx
            score = self.score(s) #vai calcular o score do novo s
            if score > melhorscore: #vai ver se este é maior que o melhor scor se for, o melhorscore passa a ser o score e a bests passa a ser a s
                melhorscore = score
                bests = list(s)
        return bests #vai dar return do s


    def roulette(self, f): #se o professor perguntar pedir a ele para explicar
        from random import random
        tot = 0.0
        for x in f: tot += (0.01+x)
        val = random()* tot #vai multiplicar total por um valor random entre [0 e 1[ , e dizer que isto n faz sentido
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] + 0.01)
            ind += 1
        return ind-1


# Exercícos da aula já com pseudo contagens ----------------------------------------------------------------------------

    def scoreEX(self, m): #responsável por calcular a contagem com as pseudo contagens
            score = 0
            motif = self.createMotifFromIndexes(m)
            motif.doCounts()
            mat = []
            for i in range(len(motif.counts)):
                linha = []
                for j in range(len(motif.counts[i])):
                    linha.append(motif.counts[i][j] + 1)
                mat.append(linha)
            for k in range(len(mat[0])):
                maxcol = mat[0][k] 
                for  f in range(1, len(mat)): 
                    if mat[f][k] > maxcol: 
                        maxcol = mat[f][k]
                score += maxcol 
            return score

    def probabSeqEX (self, seq, pwm): #vai calcular a probabilidade de a seq fazer parte deste quadro sendo que todos os elementos do quadro n tem valores negativos!

        res = 1.0
        for i in range(self.motifSize):
            lin = self.alphabet.index(seq[i])
            res *= pwm[lin][i]
        return res
    
    def mostProbableSeqEX(self, seq, pwm): #vai ver qual a posição inicial da subseq de uma seq de comprimento indefenido encaixa melhor no quandro de motifs das seqs
        maximo = -1.0
        maxind = -1
        for k in range(len(seq)-self.motifSize):
            p = self.probabSeqEX(seq[k:k+ self.motifSize], pwm)
            if(p > maximo):
                maximo = p
                maxind = k
        return maxind

    def probAllPositionsEX(self, seq, pwm): #este em vez de calcular a probabilidade de acontecer devolve uma lista com as probabilidades de acontecer em cada letra da seq
        res = []
        for k in range(len(seq)-self.motifSize+1):
            res.append(self.probabSeqEX(seq, pwm))
        return res

    def heuristicStochasticex1_al5(self):
        from random import randint

        s = [0] * len(self.seqs)
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize)
        #Passo 2
        melhorscore = self.scoreEX(s) #vai fazer o score consoante o novo score2 que não vai conter valores 0 já com as pseudos contagens
        improve = True
        while improve:
            motif = self.createMotifFromIndexes(s)
            motif.createPWM()
            newPWM = [] #vai contruir a matriz PWM sem nenhum numero negativo já com as pseudo contagens
            for k in range(len(motif.pwm)):
                linhas = []
                for t in range(len(motif.pwm[0])):
                    linhas.append(motif.pwm[k][t] + 0.1)
                newPWM.append(linhas)  
            #Passo 3
            for i in range(len(self.seqs)):
                s[i] = self.mostProbableSeqEX(self.seqs[i], newPWM)
            scr = self.scoreEX(s)
            if scr > melhorscore:
                melhorscore = scr
            else: 
                improve = False
        return s

    def gibbsEX (self, iterations = 1000):

        from random import randint
        s = [] 
        for i in range(len(self.seqs)):
             s.append(randint(0, len(self.seqs[i]) - self.motifSize -1))
        melhorscore = self.scoreEX(s)
        bests = list(s)
        for it in range(iterations):
            seq_idx = randint(0, len(self.seqs) - 1)
            seq = self.seqs[seq_idx]
            s.pop(seq_idx)
            removed = self.seqs.pop(seq_idx)
            motif = self.createMotifFromIndexes(s)
            motif.createPWM()
            newPWM = [] #vai contruir a matriz PWM sem nenhum numero negativo já com as pseudo contagens
            for k in range(len(motif.pwm)):
                linhas = []
                for t in range(len(motif.pwm[0])):
                    linhas.append(motif.pwm[k][t] + 0.1)
                newPWM.append(linhas)
            self.seqs.insert(seq_idx, removed) #vai voltar a adicionar a seq removida a lista de seqs na posição seq_idx
            r = self.probAllPositionsEX(seq, newPWM) #vai calcular a probabilidade de todas as subseqs possiveis na seq removida
            pos = self.roulette(r) #vai fazer o roulette da lista e escolher um dos valores com valores maior que 0, devolvendo a posição onde se iniciou o motif
            s.insert(seq_idx, pos) #vai adicionar o valor da pos do motif ao s na posição seq_idx
            score = self.scoreEX(s) #vai calcular o score do novo s
            if score > melhorscore: #vai ver se este é maior que o melhor scor se for, o melhorscore passa a ser o score e a bests passa a ser a s
                melhorscore = score
                bests = list(s)
        return bests #vai dar return do s

# tests

def test1():  
    sm = MotifFinding()
    sm.readFile('exemploMotifs.txt', 'dna')
    sol = [25,20,2,55,59]
    sa = sm.score(sol)
    print(sa)
    scm = sm.scoreMult(sol)
    print(scm)

def test2():
    print ("Test exhaustive:")
    seq1 = MySeq("ATAGAGCTGA","dna")
    seq2 = MySeq("ACGTAGATGA","dna")
    seq3 = MySeq("AAGATAGGGG","dna")
    mf = MotifFinding(3, [seq1,seq2,seq3])
    sol = mf.exhaustiveSearch()
    print ("Solution", sol)
    print ("Score: ", mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

    print ("Branch and Bound:")
    sol2 = mf.branchAndBound()
    print ("Solution: " , sol2)
    print ("Score:" , mf.score(sol2))
    print("Consensus:", mf.createMotifFromIndexes(sol2).consensus())
    
    print ("Heuristic consensus: ")
    sol1 = mf.heuristicConsensus()
    print ("Solution: " , sol1)
    print ("Score:" , mf.score(sol1))

def test3():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt","dna")
    print ("Branch and Bound:")
    sol = mf.branchAndBound()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

def test4():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt","dna")
    print("Heuristic stochastic")
    sol = mf.heuristicStochastic()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print ("Score mult:" , mf.scoreMult(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())
    sol2 = mf.gibbs()
    print ("Score:" , mf.score(sol2))
    print ("Score mult:" , mf.scoreMult(sol2))

def testEX():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt","dna")
    print("Heuristic stochasticEX")
    sol = mf.heuristicStochasticex1_al5()
    print ("SolutionEX: " , sol)
    print ("ScoreEX:" , mf.scoreEX(sol))
    print("ConsensusEX:", mf.createMotifFromIndexes(sol).consensus())
    sol2 = mf.gibbsEX()
    print ("Score:" , mf.scoreEX(sol2))

test1()
print('#' * 40)
test2()
print('#' * 40)
test3()
print('#' * 40)
test4()
print('#' * 40)
testEX()