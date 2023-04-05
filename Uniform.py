from RandomVariable import RandomVariable
import random

"""
Uniform RV

uniformly random value in [a,b]
"""
class Uniform(RandomVariable):
    def __init__(self,a,b):
        super().__init__()
        self.a = a
        self.b = b
        self.min = a
        self.max = b
        self.discrete = False

    def pdf(self,x):
        return 1/(self.b-self.a) if self.a <= x <= self.b else 0

    def cdf(self,x):
        if self.a <= x <= self.b:
            return (x-self.a)/(self.b-self.a)
        return 0

    def expectedValue(self):
        return (self.b + self.a) / 2

    def genVar(self):
        return random.uniform(self.a,self.b)

    def variance(self):
        return ((self.b - self.a) ** 2)/12
