import math
import random

class RandomVariable:
    def __init__(self):
        self.min = None
        self.max = None
        self.discrete = True

    def setMin(self,m):
        self.min = m

    def setMax(self,m):
        self.max = m

    def setDiscrete(self,t):
        self.discrete = t

    def isDiscrete(self,t):
        return self.discrete

    def pdf(self,a):
        pass

    def genVar(self):
        pass

    def simulate(self,k,output=False,aggregate=True):
        r = []
        for _ in range(k):
            r.append(self.genVar())
            if output:
                print(r[-1])
        if aggregate:
            print(f'Average = {sum(r)/k}')
        return r

    def simRounds(self,rounds,k,short=True,output=False,aggregate=True,):
        r = []
        for _ in range(rounds):
            r.append(self.simulate(k,output,False))
        if aggregate:
            avgs = [sum(ri)/k for ri in r]
            if not short:
                for i,a in enumerate(avgs):
                    print(f'Average round {i+1} = {a}')
            print(f'Total Average = {sum(avgs)/rounds}')

    def expectedValue(self):
        pass

    def cdf(self,k):
        pass

    def tail(self,k):
        return 1 - self.cdf(k)

class Bernoulli(RandomVariable):
    def __init__(self,p):
        super().__init__()
        self.setMin(0)
        self.setMax(1)
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

class Uniform(RandomVariable):
    def __init__(self,a,b):
        super().__init__()
        self.setMin(a)
        self.setMax(b)
        self.setDiscrete(False)
        self.a = a
        self.b = b

    def pdf(self,x):
        return 1/(self.b-self.a) if self.a <= x <= self.b else 0

    def expectedValue(self):
        return (self.b + self.a) / 2

    def genVar(self):
        return random.uniform(self.a,self.b)

class Binomial(RandomVariable):
    def __init__(self,n,p):
        super().__init__()
        self.setMin(0)
        self.setMax(n)
        self.n = n
        self.p = p
        self.qn = math.pow(1-p,n)

    def pdf(self,k):
        if k < 0 or k > self.n or k % 1:
            return 0
        return math.comb(self.n,k) * math.pow(self.p,k) * math.pow(1-self.p,self.n-k)

    def expectedValue(self):
        return self.n * self.p

    """
    Generates a Bin(n,p) random variable using the Inverse Transform Method 
    (PnC book pg. 231, "Simulation" [Ross] pg. 57).
    
    Exploits the following recursive property for pdfs of binomials:
    
        p_x(0) = (1-p)^n
        
        p_x(i+1) = p/[1-p] * [n-i]/[i+1] * p_x(i)
    
    """
    def genVar(self):
        C = self.p / (1-self.p)
        U = Uniform(0,1).genVar()
        pr = self.qn
        F = pr
        i = 0
        while U >= F:
            pr *= (C * (self.n - i) / (i + 1))
            F += pr
            if i == self.n:
                break
            i+=1
        return i

    """Uses same recursive trick as above"""
    def cdf(self,k):
        #c1 = sum([self.pdf(i) for i in range(k+1)])
        C = self.p / (1-self.p)
        pr = self.qn
        F = pr
        i = 0
        while i < k:
            pr *= (C * (self.n - i) / (i + 1))
            F += pr
            i += 1
        return min(F,1)


if __name__ == '__main__':
    y = Bernoulli(.1)
    # y.simRounds(10,10000,short=False)
    x = Binomial(100,.515)
    # print(x.pdf(10))
    z = Uniform(0,10)
    # print(z.expectedValue())
    # z.simRounds(20,100,False)
    print('x',x.genVar())
    for i in range(100):
        a = x.cdf(i)
        b = x.tail(i)
        print(a,b,a+b)

    # print(Binomial(6,.3).pdf(4))

