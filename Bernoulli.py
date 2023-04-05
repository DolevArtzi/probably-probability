from RandomVariable import RandomVariable
import random

class Bernoulli(RandomVariable):
    def __init__(self,p):
        super().__init__()
        self.p = p

    def pdf(self,a):
        if a == 1:
            return self.p
        elif a == 0:
            return 1-self.p
        return 0

    def genVar(self):
        if self.p - random.random() > 0:
            return 1
        return 0

    def expectedValue(self):
        return self.p

    def cdf(self,k):
        if k < 0:
            return 0
        if k == 1:
            return 1
        return 1 - self.p