import math

from RandomVariable import RandomVariable
from allRVs import *
from combine import Combine
class Util:
    def __init__(self):
        self.rvs = {'binomial':(Binomial,(20,.5)),
                    'uniform':(Uniform,(0,1)),
                    'bernoulli':(Bernoulli,(.5,)),
                    'geometric':(Geometric,(0.1,)),
                    'hyper geometric':(HyperGeometric, (20,20,20)),
                    'poisson':(Poisson,(12,)),
                    'exponential':(Exponential, (1/10,)),
                    'normal':(Normal, (0,1)),
                    'erlang':(Erlang, (3,1/3.5))
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

    def _avgVar(self,data):
        if not data:
            return None
        k = len(data)
        avg = sum(data) / k
        avg_var = sum([(x - avg) ** 2 for x in data]) / k
        return avg,avg_var
    def guess(self,data=None,k=None,target=None,verbose=False,map=None):
        if not map:
            map = self.rvs
        if data:
            avg,var = self._avgVar(data)
            m = {}
            for rv_name in map:
                rv, conditions = map[rv_name]
                X = rv(*conditions)
                m[str(X)] = X.expectedValue(),X.variance()
            best = float('inf')
            name = None
            r = []
            for x in m:
                diff = abs(m[x][0] - avg) + abs(m[x][1] - var)
                r.append((x,diff))
                if diff < best:
                    best = diff
                    name = x
            if verbose:
                print(r)
            print(f'Best fit: {name}')
            return name
        if k != None and target:
            data = [target.genVar() for _ in range(k)]
            return self.guess(data,verbose=verbose,map=map)
        return -1

    def improve(self,data,*conditions,X,avg,var,rv):
        alpha = 1.05
        d = 10
        m = self.calcDiff(X,*conditions,avg,var)
        best = conditions
        for i, c in enumerate(conditions):
            curr = c
            diff = self.calcDiff(X,avg,var)
            new_diff = 0
            f = 0
            for dir in [-1,1]:
                while (not f or new_diff < diff) and \
                    X.valid(curr,*tuple(list(conditions)[:i].extend(list(conditions[i+1:])))):
                    c1 = tuple(list(conditions)[:i].extend(list(conditions[i+1:])))
                    print(str(X),c1)
                    X = rv(*c1)
                    curr *= dir * alpha
                    new_diff = self.calcDiff(X,*c1,avg)
                    if new_diff < m:
                        m = new_diff
                        best = c1
        return m,best



    def calcDiff(self,X,*cond,avg,var):
        return abs(X._expectedValue(*cond) - avg) #+ abs(X.variance() - var)

    def guess2(self,data=None,k=None,target=None,verbose=False,map=None):
        if not map:
            map = self.rvs
        if data:
            avg,var = self._avgVar(data)
            m = {}
            for rv_name in map:
                rv, conditions = map[rv_name]
                X = rv(*conditions)
                # m[str(X)] = X.expectedValue(),X.variance()
                print(self.improve(data,*conditions,map,X,avg,var))
            best = float('inf')
            name = None
            r = []
            for x in m:
                diff = abs(m[x][0] - avg) + abs(m[x][1] - var)
                r.append((x,diff))
                if diff < best:
                    best = diff
                    name = x
            if verbose:
                print(r)
            print(f'Best fit: {name}')
            return name
        if k != None and target:
            data = [target.genVar() for _ in range(k)]
            return self.guess2(data,verbose=verbose,map=map)
        return -1

    def iterate(self,f,vars=None,print=False):
        if not vars:
            vars = self.rvs
        if print:
            r = []
        for rv_name in vars:
            rv, conditions = vars[rv_name]
            X = rv(*conditions)
            if print:
                r.append(f(X))
            else:
                f(X)
        if print:
            print(f'Outcomes: {r}')

    def compareAll2ndMoments(self,rv_names):
        m = {}
        for s in rv_names:
            m[s] = self.rvs[s]
        self.iterate(RandomVariable.confirm2ndMoment,vars=m)



u = Util()


if __name__ == '__main__':
    # u.guess(None,1000,Erlang(7,2),verbose=True)#map={x:u.rvs[x] for x in u.rvs if x in ['exponential','geometric']})
#     for rv_name in u.rvs:
#         print(rv_name,u.guess(None,1000,u.rvs[rv_name][0](*(u.rvs[rv_name][1]))))

    # u.simAll(60000)
    u.compareAll2ndMoments(['erlang','binomial','bernoulli','exponential'])
    # u.guess2()
    # u.guess2(None,1000,Poisson(12),verbose=True)#map={x:u.rvs[x] for x in u.rvs if x in ['exponential','geometric']})
    # X = Binomial(20,.5)
    # X.foo()