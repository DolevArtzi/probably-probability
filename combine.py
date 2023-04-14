from allRVs import *

class Combine:

    def minExp(self,X:Exponential,Y:Exponential):
        return Exponential(X.λ + Y.λ)

    def PXleqYExp(self,X:Exponential,Y:Exponential):
        return X.λ / (X.λ + Y.λ)

    """
    Assumes each X_i in vars ~ Normal(μ_i,σ^2_i) and the X_i's are independent
    """
    def SumNormal(self,vars:list[Normal]):
        return Normal(sum([x.μ for x in vars],sum([x.var for x in vars])))

    """
    Assumes each X_i in vars ~ Poisson(λ) and the X_i's are independent
    """
    def SumPoisson(self,vars:list[Poisson]):
        return Poisson(sum([x.λ for x in vars]))

    """
    Assumes each X_i in vars ~ Exp(1/λ) and the X_i's are independent
    """
    def SumExp(self,vars:list[Exponential]):
        return Erlang(len(vars),vars[0].λ)

    """
    Assumes each X_i in vars ~ Binomial(p) and the X_i's are independent
    """
    def SumBinomial(self,vars:list[Binomial]):
        return Binomial(sum([x.n for x in vars]),vars[0].p)

    """
    Assumes each X_i in vars ~ Bernoulli(p) and the X_i's are independent
    """
    def SumBernoulli(self,vars:list[Bernoulli]):
        return Binomial(len(vars),vars[0].p)

    def compare(self,X,Ys,f):
        k = 10000
        Z = f(Ys)
        X.simulate(k)
        Z.simulate(k)

c = Combine()

if __name__ == '__main__':
    X = Erlang(100,10)
    Ys = [Exponential(10) for _ in range(100)]
    c.compare(X,Ys,c.SumExp)