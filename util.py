from RandomVariable import RandomVariable
from Binomial import Binomial
from Uniform import Uniform
from Bernoulli import Bernoulli

class Util:
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

    def flipFairCoin(self,n):
        return self.flipCoin(n,.5)

    def flipCoin(self,n,p):
        return Binomial(n,p).genVar()



u = Util()

if __name__ == '__main__':
    # print(u.flipFairCoin(500))
    X = Binomial(500,.3)
    print(X.tail(130))