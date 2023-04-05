import math
import random


#random number of random variables / laplace transform/ combining rvs
class RandomVariable:
    def __init__(self):
        self.params = []
        self.min = None
        self.max = None
        self.discrete = True
        self.name = None
        pass

    def getMin(self,m):
        return self.min

    def getMax(self,m):
        return self.max
    def isDiscrete(self):
        return self.discrete

    """
    Probability Density Function 
    
    returns P[X == a]
    """
    def pdf(self,a):
        pass

    def expectedValue(self):
        pass

    """
    Cumulative Distribution Function

    P[X <= k]
    """
    def cdf(self, k):
        pass

    """
    Tail Probability

    P[X > k]
    """
    def tail(self, k):
        return 1 - self.cdf(k)


    def variance(self):
        pass

    """
    Generates an instance of a random variable, given the distribution.
    
    Similar to Mathematica's RandomVariate[..] function.
    """
    def genVar(self):
        pass

    """
    Simulates k independent generations of the random variable
    
    - output: if true, will print each generated value  
    - aggregate: if true, will print the average value
    """
    def simulate(self,k,output=False,aggregate=True):
        r = []
        for _ in range(k):
            r.append(self.genVar())
            if output:
                print(r[-1])
        if aggregate:
            print(f'Average = {sum(r)/k}')
            if output:
                print(f'Outcomes: {r}')
        return r

    """
    Simulates k independent generations of the random variable, "rounds" times. 
    
    - short: if false (and aggregate is true), will print the average value for each round
    - output: if true, will print each generated value  
    - aggregate: if true, will print the average value across all rounds
    """
    def simRounds(self,rounds,k,short=True,output=False,aggregate=True):
        r = []
        for _ in range(rounds):
            r.append(self.simulate(k,output,False))
        if aggregate:
            avgs = [sum(ri)/k for ri in r]
            if not short:
                for i,a in enumerate(avgs):
                    print(f'Average round {i+1} = {a}')
            print(f'Total Average = {sum(avgs)/rounds}')

    def _paramString(self):
        s = ''
        for p in self.params[:-1]:
            s += str(p) + ','
        return s + str(self.params[-1])

    def __str__(self):
        return f'{self.name.capitalize()}({self._paramString()})'