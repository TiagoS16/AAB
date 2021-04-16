from Indiv import Indiv, IndivInt, IndivReal
from random import random


class Popul:

    def __init__(self, popsize, indsize, indivs=[]):#nao passmos um gene
        self.popsize = popsize# numero de individuos da populacao (10 listas)
        self.indsize = indsize#tamanho dos individuos (cada individuo (lista) com 5 elementos)
        if indivs:#se os individuos forem fornecidos
            self.indivs = indivs #individuos
        else:
            self.initRandomPop()#se nao temos de gerar de forma aleatoria

    def getIndiv(self, index):#ir buscar um individuo x
        return self.indivs[index]#index = x, vai dar a posicao desse individuo

    def initRandomPop(self):#gerar individuos de forma aleatoria
        self.indivs = []
        for _ in range(self.popsize):#quantidade de listas a gerar
            indiv_i = Indiv(self.indsize, [])#gerar os individuos aleatoriamente (n de elemntos, lista)
            self.indivs.append(indiv_i)#adicionar os individuos a lista

    def getFitnesses(self, indivs=None):#ir buscar a todas as fitness dos individuos(valores de aptidao)
        fitnesses = []#abrir lista de fitnesses
        if not indivs:# se nao forem inseridos os individuos
            indivs = self.indivs
        for ind in indivs:# se forem inseridos individuos
            fitnesses.append(ind.getFitness())#adicionar o fitness à lista
        return fitnesses

    def bestSolution(self):# melhor solucao dos individuos
        return max(self.indivs)

    def bestFitness(self):#individuo que tem a avaliacao maxima
        indv = self.bestSolution()#melhor solucao
        return indv.getFitness()#dar o fitness dessa solucao


    def selection(self, n, indivs=None):#mecanismo de selecao para reproducao
        res = []
        fitnesses = list(self.linscaling(self.getFitnesses(indivs)))#vai obter os fitnesses dos individuos e fazer a normalizacao
        for _ in range(n):# n = numero de novos descendentes
            sel = self.roulette(fitnesses)#selecao atraves da roleta (sel = posicao do fitnesse)
            fitnesses[sel] = 0.0 #
            res.append(sel)
        return res

    def roulette(self, f):#f = lista ja das somas dos individuos ??
        tot = sum(f)#soma de f
        val = random()#melhor valor de selecao/aptidao ??
        acum = 0.0#acumulacao de valores de aptidao
        ind = 0#inicializacao de individuos
        while acum < val:
            acum += (f[ind] / tot)#acumulacao
            ind += 1 #somar um individuo
        return ind-1#??

    def linscaling(self, fitnesses):#normalizacao do valor de aptidao para [0,1]
        mx = max(fitnesses)#maximo valor de aptidao
        mn = min(fitnesses)#valor minimo de apridao
        res = []#lista de fitnesses normalizado
        for f in fitnesses:
            val = (f-mn)/(mx-mn)
            res.append(val)
        return res
        #exemplo:
        #fitnesses = [1,2,3,4]
        #(1-1)/(4-1) = 0.0 ! (2-1)/(4-1)=0.33 |...
        #res = [0.0, 0.3333333333333333, 0.6666666666666666, 1.0]

    def recombination(self, parents, noffspring):#nooffspring = quantas novas solucoes queremos gerar a partir da populacao existente
        offspring = []
        new_inds = 0#inicializacao de novos individuos
        while new_inds < noffspring:
            parent1 = self.indivs[parents[new_inds]]#ir buscar um progenitor 1 aos individuos
            parent2 = self.indivs[parents[new_inds+1]]#ir buscar um progenitor 2 aos individuos
            offsp1, offsp2 = parent1.crossover(parent2)#fazer o cruzamento entre o progenitor 1 e 2
            offsp1.mutation()#aplica mutacao a nova geracao
            offsp2.mutation()#aplica mutacao a nova geracao
            offspring.append(offsp1)#adicionar a lista de novos descendentes
            offspring.append(offsp2)#adicionar a lista de novos descendentes
            new_inds += 2
        return offspring

    def reinsertion(self, offspring):#mecanismo de reinsercao -> selecao dos individuos que vao constituir a populacao OU iteracao seguinte
        #offspring = descendentes
        #Exemplo= tenho uma pop com 100 individuos
        #quero 50 descendentes mas para completar a geracao seguinte ainda me faltam 50, ENTAO faco a selecao(roleta)
        tokeep = self.selection(self.popsize-len(offspring))#selecao de individuos
        ind_offsp = 0
        for i in range(self.popsize):
            if i not in tokeep:
                self.indivs[i] = offspring[ind_offsp]#preencher o resto da pop com novos individuos
                ind_offsp += 1


class PopulInt(Popul):

    def __init__(self, popsize, indsize, ub, indivs=[]):
        self.ub = ub
        Popul.__init__(self, popsize, indsize, indivs)

    def initRandomPop(self):
        self.indivs = []
        for _ in range(self.popsize):#quantidade de listas a gerar
            indiv_i = IndivInt(self.indsize, [], 0, self.ub)#diferenca IndivInt #gerar os individuos aleatoriamente (n de elemntos, lista)
            self.indivs.append(indiv_i)#adicionar os individuos a lista


class PopulReal(Popul):

    def __init__(self, popsize, indsize, lb=0.0, ub=1.0, indivs=[]):
        # completar
        self.lb = lb
        self.ub = ub
        Popul.__init__(self, popsize, indsize, indivs)


    def initRandomPop(self):
        # completar
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = IndivReal(self.indsize, [], lb = self.lb, ub = self.ub)
            self.indivs.append(indiv_i)
        pass
