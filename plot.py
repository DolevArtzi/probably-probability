from allRVs import *
from util import Util
from matplotlib import pyplot as plt
from collections import Counter

util = Util()
class Plot:
    def plotPDF(self,X:RandomVariable,mx=None,δ=0.05):
        self.plot({X.name:([X.params],mx if mx != None else 2 * X.expectedValue(),δ)},'pdf')

    def plotCDF(self,X:RandomVariable,mx=None,δ=0.05):
        self.plot({X.name:([X.params],mx if mx != None else 2 * X.expectedValue(),δ)},'cdf')


    """
    m: a map of the form
        k: RV class name (eg 'binomial')
        v: (conditions, mx, δ)
        
        conditions: a list of parameters to be instantiated with k eg. [(20,.5), (20,.7)]
        mx = max value to plot for distribution k
        δ = step value for calculation

    f: the name of a function of type Real --> Real that belongs to all RVs (eg pdf or cdf)
    
    together: 
        true: all plotted on same graph
        false: different graphs for each instance
    """
    def plot(self,m,f,together=True):
        legend = []
        m = {util.rvs[k][0]:m[k] for k in m}
        for rv in m:
            print(m)
            conditions, mx, δ = m[rv]
            for c in conditions:
                print(rv)
                print(rv(*c))
                X = rv(*c)
                self._plot(X,mx,δ,f)
                if not together:
                    plt.legend([f'{X}'])
                    plt.show()
                    plt.close()
                else:
                    legend.append(f'{X}')
        if together:
            plt.legend(legend)
            plt.show()
            plt.close()

    def _plot(self,X,mx,δ,f):
        x, y = [],[]
        m1 = X.getMin()
        MAX = 400
        i = 0
        if not X.strictLower:
            if m1 == -float('inf'):
                μ = X.expectedValue()
                if μ > 0:
                    m1 = .4 * μ
                else:
                    m1 = 2.5 * μ
            m1 += δ
        if X.isDiscrete():
            δ = max(δ,1)
        while m1 <= mx and i <= MAX:
            x.append(m1)
            F = getattr(X,f)
            y.append(F(m1))
            print(x[-1],y[-1])
            m1+=δ
            i+=1
        plt.plot(x, y)

    """
    Compares k samples of X to the scaled pdf of X graphically
    """
    def plotSamples(self,X,k=10000):
        r,s = X.simulate(k)
        counts = Counter(r)
        print(counts)
        x = []
        y = []
        for val in counts:
            x.append(val)
            y.append(100 * counts[val]/k)
        plt.legend([f'{X} sampled {k} times'])
        plt.scatter(x,y)
        self._plot(X, 2 * X.expectedValue(), 1 if X.isDiscrete() else 0.05, 'scaledPdf')
        plt.text(12, 10.5,s)
        plt.xlabel(f'Value of {X}')
        plt.ylabel(f'P[X = x] (%)')
        plt.title(f'Sample of {X} for {k} iters vs. {"pmf" if X.isDiscrete() else "pdf"} of X (%)')
        plt.show()
        plt.close()


if __name__ == '__main__':
    P = Plot()
    # P.plot({'binomial':([(20,.3),(20,.5),(20,.7)],20,1)},'pdf')
    # P.plotSamples(Normal(10,10),10000)
    P.plotPDF(Normal(10,16),25,.05)
    # P.plotSamples(Poisson(10),10000)
    # P.plotPDF(Erlang(3,1/3.5),1,.01)
    # P.plot({'uniform':([(0,1)],5,1)},'moment')
    # for i in range(1,6):
    #     print(Uniform(0,10).moment(i))
    X = Normal(-10,400)
    print(X.pdf(14))