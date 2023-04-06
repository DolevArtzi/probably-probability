from RandomVariable import RandomVariable
from Uniform import Uniform
import math

"""
Binomial RV

Number of successes in n independent trails with success probability p in each trial
"""
class Binomial(RandomVariable):
    def __init__(self, n, p):
        super().__init__()
        self.min = 0
        self.max = n
        self.n = n
        self.p = p
        self.qn = math.pow(1 - p, n)
        self.params.append(n)
        self.params.append(p)
        self.name = 'binomial'

    def pdf(self, k):
        if k < 0 or k > self.n or k % 1:
            return 0
        return math.comb(self.n, k) * math.pow(self.p, k) * math.pow(1 - self.p, self.n - k)

    def expectedValue(self):
        return self.n * self.p

    def variance(self):
        return self.n * self.p * (1 - self.p)

    """
    Generates a Bin(n,p) random variable using the Inverse Transform Method 
    (PnC book pg. 231, "Simulation" [Ross] pg. 57).

    Exploits the following recursive property for pdfs of binomials:

        p_x(0) = (1-p)^n

        p_x(i+1) = p/[1-p] * [n-i]/[i+1] * p_x(i)

    """
    def genVar(self):
        C = self.p / (1 - self.p)
        U = Uniform(0, 1).genVar()
        pr = self.qn
        F = pr
        i = 0
        while U >= F:
            pr *= (C * (self.n - i) / (i + 1))
            F += pr
            if i == self.n:
                break
            i += 1
        return i

    """Uses same recursive trick as above"""
    def cdf(self, k):
        if k < 0:
            return 0
        if k > self.n:
            return 1
        C = self.p / (1 - self.p)
        pr = self.qn
        F = pr
        i = 0
        while i < k:
            pr *= (C * (self.n - i) / (i + 1))
            F += pr
            i += 1
        return min(F, 1)

if __name__ == '__main__':
    x = Binomial(100,0.01)
    print(x.simulate(50,False))
    print(Binomial(100,.34).variance())


