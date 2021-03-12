# -*- coding: utf-8 -*-

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
        self.occ = {}
        for c in self.alphabet:
            self.occ[c] = -1
        for i in range(len(self.pattern)):
            self.occ[self.pattern[i]] = i

            
    def process_gsr(self):
        '''Implementação do Good Suffix Rule'''
        self.f = [0] * (len(self.pattern) + 1)
        self.s = [0] * (len(self.pattern) + 1)
        i = len(self.pattern)
        j = i + 1
        self.f[i] = j
        while i > 0:
            while j <= len(self.pattern) and self.pattern[i-1] != self.pattern[j-1]:
                if self.s[j] == 0:
                    self.s[j] = j - i
                j = self.f[j]
            i = i - 1
            j -= 1
            self.f[i] = j
        j = self.f[0]
        for i in range(len(self.pattern)):
            if self.s[i] == 0:
                self.s[i] = j
            if i == j:
                self.f[j]

        
        
    def search_pattern(self, text):
        res = []
        i = 0
        while i <= (len(text) - len(self.pattern)):
            j = len(self.pattern) - 1
            while j >= 0 and self.pattern[j] == text[j+i]:
                j -= 1
            if j < 0:
                res.append(i)
                i = i + self.s[0]
            else:
                c = text[j+i]
                i += max(self.s[j+1], j-self.occ[c])
        return res

def wtest():
    bm = BoyerMoore("ACTG", "ACCA")
    print (bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC"))

wtest()

# result: [5, 13, 23, 37]
            
