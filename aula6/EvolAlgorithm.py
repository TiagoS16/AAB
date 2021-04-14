from Popul import Popul


class EvolAlgorithm:

    def __init__(self, popsize, numits, noffspring, indsize):
        self.popsize = popsize#tamanho da pop
        self.numits = numits # numero de iteracoes
        self.noffspring = noffspring #numero de novos descendentes
        self.indsize = indsize#tamanho dos individuos

    def initPopul(self, indsize):#geracao de uma pop inicial
        self.popul = Popul(self.popsize, indsize)#tamanho da pop e dos ind

    def evaluate(self, indivs):#avaliacao
        for i in range(len(indivs)):#defenir a funcao de avaliacao para cada ind
            ind = indivs[i]
            fit = 0.0
            for x in ind.getGenes():#para cada ind vai buscar a sus representacao (vetor de 0 e 1)
                if x == 1: #percorre o vetor to+do
                    fit += 1.0 #adiciona
            ind.setFitness(fit) #quando acaba atribui essa fitness ao individuo
        return None

    def iteration(self):#iteracao (estrutura do algoritmo evolucionario)
        parents = self.popul.selection(self.noffspring)#selecao para reproducao
        offspring = self.popul.recombination(parents, self.noffspring)#nova geracao atraves da recombinacao
        self.evaluate(offspring)#avaliar a populacao
        self.popul.reinsertion(offspring)#fazer a reinsercao (selecao dos individuos que vao constituir a populacao OU iteracao seguinte
        #continuar ate atingir o criterio de paragem

    def run(self):
        self.initPopul(self.indsize)#criar a pop inicial
        self.evaluate(self.popul.indivs)#avaliar essa pop
        self.bestsol = self.popul.bestSolution()#solucao inicial
        for i in range(self.numits+1):#numero de iteracoes +1 porque o range n inclui a ultima
            self.iteration()#fazer a iteracao
            bs = self.popul.bestSolution()#atualizar a solucao
            if bs > self.bestsol:#avaliar a nova solucao
                self.bestsol = bs
            print("Iteration:", i, " ", "Best: ", self.bestsol)

    def printBestSolution(self):
        print("Best solution: ", self.bestsol.getGenes())
        print("Best fitness:", self.bestsol.getFitness())


def test():
    ea = EvolAlgorithm(100, 20, 50, 10)
    ea.run()
def test1():
    ea = EvolAlgorithm(100, 20, 50, 100)#mais complexo porque tem mais individuos (100)
    ea.run()

if __name__ == "__main__":
    #test()
    test1()
