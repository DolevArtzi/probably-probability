from allRVs import *
from util import Util
from matplotlib import pyplot as plt

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

    f: the name of a function of type RandomVariable -> Real Numbers that belongs to all RVs
    
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
        MAX = 200
        i = 0
        if not X.strictLower:
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

if __name__ == '__main__':
    P = Plot()
    P.plotPDF(Geometric(.01))
