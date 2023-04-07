import math

from RandomVariable import RandomVariable
from Binomial import Binomial
from Uniform import Uniform
from Bernoulli import Bernoulli
from Geometric import Geometric
from HyperGeometric import HyperGeometric

class Util:
    def __init__(self):
        self.rvs = {'binomial':(Binomial,(20,.5)),
                    'uniform':(Uniform,(0,1)),
                    'bernoulli':(Bernoulli,(.5,)),
                    'geometric':(Geometric,(0.1,)),
                    'hyper geometric':(HyperGeometric, (20,20,20))
                    }

    """
    Markov's Inequality

    P[X >= a] <= E[X] / a

    if X is a non-negative RV and a > 0 (finite mean)
    """
    def markovs(self,X,a):
        if a > 0:
            return X.expectedValue() / a

    """
    Chebyshev's Inequality
    
    P[|X - E[X]| >= a] <= Var(x)/a^2 (finite mean, variance, a > 0)
    """
    def chebyshevs(self,X,a):
        if a > 0:
            return X.variance() / (a * a)

    def hoeffdingsBin(self,X,λ,upperTail=True):
        μ = X.expectedValue()
        if upperTail:
            return math.exp(-(λ**2)/(2*μ + λ))
        return math.exp(-(λ**2)/(3*μ))

    """
    Sn = Σ_i X_i, X_i independent RVs in [0,1]
    E[Sn] = μ
    then for all λ >= 0: 
        
        P[Sn >= μ + λ] <= e^(-λ^2/(2μ + λ))
        
        P[Sn <= μ - λ] <= e^(-λ^2/3μ)
    
    """
    def hoeffdings(self,Sn,λ,upperTail=True):
        μ = sum([X.expectedValue() for X in Sn])
        if upperTail:
            return math.exp(-(λ**2)/(2*μ + λ))
        return math.exp(-(λ**2)/(3*μ))

    def flipFairCoin(self,n):
        return self.flipCoin(n,.5)

    def flipCoin(self,n,p):
        return Binomial(n,p).genVar()

    """
    Generates k random instances of each distribution in self.rvs, and displays the averages
    
    """
    def simAll(self,k):
        res = []
        avgs = {}
        print('=' * 75)
        print(f'---  Statistics for k = {k} iterations ---')
        for rv_name in self.rvs:
            rv, conditions = self.rvs[rv_name]
            X = rv(*conditions)
            r = X.simulate(k)
            res.append(r)
            if r:
                avgs[rv_name] = sum(r) / k
            else:
                avgs.append(0)
            # print(f'{X}: Average = {avgs[rv_name]:.4f}')
        print('=' * 75)

    """
    Returns a random instance of an RV given the name of the distribution and its necessary parameters
    """
    def generateRV(self,rv_name,*conditions,display=True):
        rv = self.rvs[rv_name][0]
        X = rv(*conditions)
        y = X.genVar()
        if display:
            print(f'{X}: {y}')
        return y

u = Util()

if __name__ == '__main__':
    u.simAll(10000)