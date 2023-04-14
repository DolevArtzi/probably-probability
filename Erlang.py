from RandomVariable import RandomVariable
import math
from Uniform import Uniform
from mathutil import LIGF
class Erlang(RandomVariable):

    def __init__(self,k,λ):
        super().__init__()
        self.min = -float('inf')
        self.max = float('inf')
        self.λ = λ
        self.k = k
        self.params.append(k)
        self.params.append(λ)
        self.name = 'erlang'

    def _valid(self,*params):
        k = params[0]
        λ = params[1]
        return 0 < k == int(k) and λ > 0

    def pdf(self,a):
        if a >= 0:
            return math.pow(self.λ,self.k) * math.pow(a,self.k-1) * math.exp(-self.λ*a)/(math.factorial(self.k-1))
        return 0

    def cdf(self, x):
        return LIGF(self.k,self.λ*x)/math.factorial(self.k-1)

    def expectedValue(self):
        return self.k / self.λ

    def _expectedValue(self,*params):
        k = params[0]
        λ = params[1]
        return k/λ

    def variance(self):
        return self.k / (self.λ ** 2)

    def genVar(self):
        urvs = [Uniform(0,1).genVar() for _ in range(self.k)]
        product = 1
        for x in urvs: product *= x
        return -(1/self.λ) * math.log(product)

if __name__ == '__main__':
    X = Erlang(80,2)
    print(X.cdf(40))
