from EvolAlgorithm import EvolAlgorithm
from Popul import PopulInt, PopulReal
from MotifFinding import MotifFinding
from MyMotifs import MyMotifs


def createMatZeros(nl, nc):
    res = []
    for _ in range(0, nl):
        res.append([0]*nc)
    return res


def printMat(mat):
    for i in range(0, len(mat)):
        for j in range(len(mat[i])):
            print(f"{mat[i][j]:.3f}", end=' ')
        print()


class EAMotifsInt (EvolAlgorithm):
    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = len(self.motifs)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize):
        #maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulInt(self.popsize, indsize, maxvalue, [])
    
    def evaluate(self, indivs):#mudar a funcao de avalicao -> usamos o score
        for i in range(len(indivs)):
            ind = indivs[i]#cada vetor de posicoes
            sol = ind.getGenes()
            fit = self.motifs.score(sol)#avaliar o score que sera a fit para cada vetor de posicoes iniciais
            ind.setFitness(fit)


class EAMotifsReal (EvolAlgorithm):
    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = self.motifs.motifSize * len(self.motifs.alphabet)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulReal(self.popsize, indsize,maxvalue, [])

    def vec_to_pwm(self,v):
        n_alph = len(self.motifs.alphabet)
        n_motif = self.motifs.motifSize

        pwm = createMatZeros(len(n_alph),n_motif)

        for i in range(0,len(v),n_alph): #
            col_idx = i / n_alph
            col = v[i:i+n_alph]
            soma = sum(col)
            for j in range(n_alph):
                pwm[j][col_idx] = col[j] / soma

        #EXEMPLO:
        #[1,2,3,4,5,6,7,8,9,10,....]

        #A 1
        #C 2
        #T 3
        #G 4
        
        #A 1 2 3 4
        #C
    
    def evaluate(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            #criar um MyMotif a partir da PWM
            pwm = self.vec_to_pwm(sol)
            mtf=MyMotifs(pwm=pwm, alphabet=self.motifs_finding.alphabet)
            s = []
            for j in range(len(self.motifs_finding.seqs)):
                seq=self.motifs_finding.seqs[j].seq
                p = mtf.motifs.mostProbableSeq(seq)
                s.append(p)
            ## TPC - ussar score multiplicativo sem atualizar a PWM ##
            fit = self.motifs_finding.score(s)
            ind.setFitness(fit)

def test1():
    ea = EAMotifsInt(100, 1000, 50, "exemploMotifs.txt")
    ea.run()
    ea.printBestSolution()


def test2():
    ea = EAMotifsReal(100, 2000, 50, "exemploMotifs.txt")
    ea.run()
    ea.printBestSolution()


#test1()
test2()
