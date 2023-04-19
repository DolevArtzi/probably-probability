import math

from allRVs import *
from util import Util
from matplotlib import pyplot as plt
from collections import Counter

util = Util()
class Plot:
    def _fillInPDFCDFTail(self,X,name,text=None,show=True):
        print(name)
        t = '=='
        if name == 'cdf':
            t = '<='
        elif name == 'tail':
            t = '>'

        m = {
            'xlabel' : f'Value of {X}',
            'ylabel': f'P[X {t} x]',
            'title': f'{name} of {X}',
        }

        if text:
            m['text'] = text
        self.fillInChartInfo(m)
        if show:
            self._showPlt()

    def _showPlt(self):
        plt.show()
        plt.close()

    def plotPDF(self,X:RandomVariable,mx=None,mn=None,δ=0.05):
        self.plot({X.name:([X.params],mx if mx != None else 2 * X.expectedValue(),mn,δ)},'pdf',dontShow=True)
        self._fillInPDFCDFTail(X,'pmf' if X.isDiscrete() else 'pdf')

    def plotTail(self,X:RandomVariable,mx=None,mn=None,δ=0.05):
        self.plot({X.name:([X.params],mx if mx != None else 2 * X.expectedValue(),mn,δ)},'tail',dontShow=True)
        self._fillInPDFCDFTail(X,'tail')

    def plotCDF(self,X:RandomVariable,mx=None,mn=None,δ=0.05):
        self.plot({X.name:([X.params],mx if mx != None else 2 * X.expectedValue(),mn,δ)},'cdf',dontShow=True)
        self._fillInPDFCDFTail(X,'cdf')

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
    def plot(self,m,f,together=True,dontShow=False):
        legend = []
        m = {util.rvs[k][0]:m[k] for k in m}
        for rv in m:
            conditions, mx, mn, δ = m[rv]
            for c in conditions:
                X = rv(*c)
                self._plot(X,mx,mn,δ,f)
                if not together:
                    plt.legend([f'{X}'])
                    if not dontShow:
                        self._showPlt()
                else:
                    legend.append(f'{X}')
        if together:
            plt.legend(legend)
            if not dontShow:
                self._showPlt()

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
        plt.scatter(x,y)
        self._plot(X, 2 * X.expectedValue(),None, 1 if X.isDiscrete() else 0.2, 'pdf')
        self.fillInChartInfo(m)
        self._showPlt()

if __name__ == '__main__':
    P = Plot()
    # P.plot({'binomial':([(20,.3),(20,.5),(20,.7)],20,0,1)},'pdf')
    P.plotTail(Exponential(.10),mx=50,mn=0)