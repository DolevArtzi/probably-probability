from RandomVariable import RandomVariable
import random

class Uniform(RandomVariable):
    def __init__(self,a,b):
        super().__init__()
        self.a = a
        self.b = b

    def pdf(self,x):
        return 1/(self.b-self.a) if self.a <= x <= self.b else 0

    def expectedValue(self):
        return (self.b + self.a) / 2

    def genVar(self):
        return random.uniform(self.a,self.b)
