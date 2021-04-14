from random import randint, random, shuffle, uniform


class Indiv:

    def __init__(self, size, genes=[], lb=0, ub=1): #o que caracteriza o individuo sao so seus genes e o fitness(valor de aptidao)| lb e ub sao o intervalo de valores que cada gene pode ter
        self.lb = lb #lower bound - limite inferior do gene 0-binario
        self.ub = ub #upper bound - limite superior do gene 1- binario
        self.genes = genes #genoma (informacao de to+do o individuo)
        self.fitness = None #guarda valor de aptidão (fitness)
        if not self.genes:#se nao for fornecida nenhuma lista de genes
            self.initRandom(size)#geramos um individuo de forma aleatoria

    # comparadores.
    # Permitem usar sorted, max, min (sobre a nossa populacao, em que a comparacao e feita com base na futness- qualidade das solucoes)

    def __eq__(self, solution):
        if isinstance(solution, self.__class__):
            return self.genes.sort() == solution.genes.sort()
        return False

    def __gt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness > solution.fitness
        return False

    def __ge__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness >= solution.fitness
        return False

    def __lt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness < solution.fitness
        return False

    def __le__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness <= solution.fitness
        return False

    def __str__(self):
        return f"{str(self.genes)} {self.getFitness()}"

    def __repr__(self):
        return self.__str__()

    def setFitness(self, fit):
        self.fitness = fit

    def getFitness(self):
        return self.fitness

    def getGenes(self):
        return self.genes

    def initRandom(self, size):#gerar individuos de uma forma aleatoria 
        self.genes = []
        for _ in range(size):#size - e o numero de individuos(populacao), ou seja, a nossa solucao
            self.genes.append(randint(self.lb, self.ub))# gerar individuos aleatorios entre 0 e 1 (caso seja binario)

    def mutation(self):#mutacao sobre um vetor de valores binario
        s = len(self.genes)# genes = [0,1,0,1,0,1]
        pos = randint(0, s-1)#gera uma posicao -> s-1 porque o len comeca a contar do 1 e no randint e inclusive
        if self.genes[pos] == 0:#se tiver 0
            self.genes[pos] = 1#passamos para 1
        else:
            self.genes[pos] = 0# ou ao contrario, se tive 1 passamos para 0
        #exemplo:
            #progenitor: [0,1,1,0,0,1,0,1] pos = 4, na pos 4 temos um o entao vai trocar para 1
            #descendente: [0,1,1,0,1,1,0,1]-> trocou para 1
            
    def crossover(self, indiv2):#cruzamento de um ponto
        return self.one_pt_crossover(indiv2)

    def one_pt_crossover(self, indiv2):#dar indiv2 para ter o cruzamento
        #construcao de novo individuo
        offsp1 = []#descendente 1
        offsp2 = []#descendente 2
        s = len(self.genes)#contar os elementos
        pos = randint(0, s-1)#selecionar uma posicao
        for i in range(pos):
            offsp1.append(self.genes[i])#mantem igual ate pos-1 -> exemplo: pos = 4, vai manter ate a posicao 3
            offsp2.append(indiv2.genes[i])#mantem igual ate pos-1
        for i in range(pos, s):
            offsp2.append(self.genes[i])#troca de pos ate ao fim (progenitor 2 troca com 1)
            offsp1.append(indiv2.genes[i])#troca de pos ate ao fim (progenitor 1 troca com 2)
        res1 = self.__class__(s, offsp1, self.lb, self.ub)#permite que eu posso usar o mesmo metodo dentro de uma representacao inteira
        res2 = self.__class__(s, offsp2, self.lb, self.ub)#vou criar uma nova instancia mas com base na representacao do novo
        return res1, res2


class IndivInt (Indiv):

    def __init__(self, size, genes=[], lb=0, ub=1):#ub = tamanho da seq menos o tamanjo do motif
        self.lb = lb
        self.ub = ub
        self.genes = genes
        self.fitness = None
        if not self.genes:
            self.initRandom(size)

    def initRandom(self, size):#gerar os individuos aleatoriamente
        self.genes = []
        for _ in range(size):
            self.genes.append(randint(0, self.ub))

    def mutation(self):
        s = len(self.genes)#len dos genes
        pos = randint(0, s-1)#escolher uma posicao aleatoria
        self.genes[pos] = randint(0, self.ub)#substituir esse posicao por um valor aleatorio ente 0 e ub


class IndivReal(Indiv):

    def initRandom(self, size):
        self.genes = []
        for _ in range(size):
            self.genes.append(uniform(self.lb,self.ub))

    def mutation(self):
        s = len(self.genes)
        pos = randint(0,s-1)
        self.genes[pos] = uniform(self.lb,self.ub)
