from allRVs import *
from plot import Plot

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


    def binMaxPlot(self,vars,k):
        P = Plot()
        m = {
            'f': lambda vs: max(X.genVar() for X in vs),
            'prefixArgs': [vars],
            'iters': k
        }
        l = len(vars)
        chart = {
            'xlabel' : f'iteration i',
            'ylabel': f'Max Across {vars[0]}s',
            'title': f'Max Value for {l} {vars[0]}s for {k} Iterations',
        }

        P.plotGeneric(fInfo=m,chart=chart,addStats=True)

    # def binMaxPlotIterative(self,vars,mn,mx,k,δ=None):
    #     P = Plot()
    #     m = {
    #         'f': :,
    #         'prefixArgs': [vars,k],
    #         'mn':mn,
    #         'mx':mx,
    #         'δ':δ if δ else max(int((mx - mn)/100)+1,1)
    #     }
    #     l = len(vars)
    #     chart = {
    #         'xlabel' : f'Number of iterations, x',
    #         'ylabel': f'Average value of the max across {vars[0]}s',
    #         'title': f'Average Max Value for {l} {vars[0]}s for {k} Iterations for range ({mn},{mx},{δ})',
    #     }
    #     print(m['δ'])
    #     P.plotGeneric(fInfo=m,chart=chart,addStats=True)


    def compare(self,X,Ys,f):
        k = 10000
        Z = f(Ys)
        X.simulate(k)
        Z.simulate(k)

c = Combine()

if __name__ == '__main__':
    # X = Erlang(100,10)
    # Ys = [Exponential(10) for _ in range(100)]
    # c.compare(X,Ys,c.SumExp)
    vars = [Binomial(20,.5) for _ in range(20)]
    c.binMaxPlot(vars,100)
    # c.binMaxPlotIterative(vars,100,10000,100)