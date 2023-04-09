from RandomVariable import RandomVariable
import math
from Uniform import Uniform

class Exponential(RandomVariable):

    def __init__(self,λ):
        super().__init__()
        self.min = 0
        self.max = float('inf')
        self.λ = λ
        self.params.append(λ)
        self.name = 'exponential'
        self.eNegλ = math.exp(-λ)

    def pdf(self,a):
        if a <= 0:
            return 0
        return self.λ * math.pow(self.eNegλ,a)

    def cdf(self, k):
        if k > 0:
            return 1 - math.pow(self.eNegλ,k)
        return 0

    def expectedValue(self):
        return 1/self.λ

    def variance(self):
        return 1/(self.λ ** 2)

    def genVar(self):
        return -(1/self.λ) * math.log(Uniform(0,1).genVar())