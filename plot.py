import math

from allRVs import *
from util import Util
from matplotlib import pyplot as plt
from collections import Counter

util = Util()
class Plot:
    def plotPDF(self,X:RandomVariable,mx=None,mn=None,δ=0.05):
        print('ok',mn)
        self.plot({X.name:([X.params],mx if mx != None else 2 * X.expectedValue(),mn,δ)},'pdf')

    def plotCDF(self,X:RandomVariable,mx=None,mn=None,δ=0.05):
        self.plot({X.name:([X.params],mx if mx != None else 2 * X.expectedValue(),mn,δ)},'cdf')


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
    def plot(self,m,f,together=True,mn=None):
        print('yo',mn)
        legend = []
        m = {util.rvs[k][0]:m[k] for k in m}
        for rv in m:
            print(m)
            conditions, mx, mn, δ = m[rv]
            for c in conditions:
                print(rv)
                print(rv(*c))
                X = rv(*c)
                self._plot(X,mx,mn,δ,f)
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

    def _plot(self,X,mx,mn,δ,f):
        x, y = [],[]
        m1 = X.getMin()
        MAX = 400
        i = 0
        if mn != None:
            m1 = mn
        if not X.strictLower:
            if m1 == -float('inf'):
                μ = X.expectedValue()
                if μ > 0:
                    m1 = .4 * μ
                elif μ < 0:
                    m1 = 2.5 * μ
                else:
                    m1 = -math.sqrt(X.variance())
            m1 += δ
        if X.isDiscrete():
            δ = max(δ,1)
        while m1 <= mx and i <= MAX:
            x.append(m1)
            F = getattr(X,f)
            y.append(F(m1))
            m1+=δ
            i+=1
        plt.plot(x, y)

    def fillInChartInfo(self,m):
        x0,x1 = plt.xlim()
        y0,y1 = plt.ylim()
        x,y = .6*(x1-x0),.6*(y1-y0)
        for k in m:
            f = getattr(plt,k)
            if k == 'text':
                f(x,y,m[k])
            else:
                f(m[k])


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
            y.append(counts[val]/k)

        m = {
            'xlabel' : f'Value of {X}',
            'ylabel': f'P[X = x]',
            'title': f'Sample of {X} for {k} iters vs. {"pmf" if X.isDiscrete() else "pdf"} of X',
            'text': s
        }
        print('hi',plt.xlabel)
        plt.scatter(x,y)
        self._plot(X, 2 * X.expectedValue(),None, 1 if X.isDiscrete() else 0.2, 'pdf')
        self.fillInChartInfo(m)
        # # plt.legend([f'{X} sampled {k} times'])
        # plt.xlabel(f'Value of {X}')
        # plt.ylabel(f'P[X = x] (%)')
        # plt.title(f'Sample of {X} for {k} iters vs. {"pmf" if X.isDiscrete() else "pdf"} of X (%)')
        # # plt.text(15,0.09,'hey')
        plt.show()
        plt.close()


if __name__ == '__main__':
    P = Plot()
    # P.plot({'binomial':([(20,.3),(20,.5),(20,.7)],20,1)},'pdf')
    # P.plotSamples(Normal(10,10),10000)



    # P.plotPDF(Normal(0,100),30,.05)



    # P.plotSamples(Binomial(20,.5),10000)
    P.plotSamples(Normal(0,1),10000)
    # P.plotCDF(Normal(0,9),mx=10,mn=-10,δ=.2)

    # P.plotPDF(Erlang(3,1/3.5),1,.01)
    # P.plot({'uniform':([(0,1)],5,1)},'moment')
    # for i in range(1,6):
    #     print(Uniform(0,10).moment(i))