from allRVs import *
from util import Util
from combine import Combine

util = Util()
combine = Combine()

from matplotlib import pyplot as plt


class Plot:
    def plotPDF(self,X:RandomVariable,δ=0.05,conditions=None,m=None,other_name=None,other_δ=None):
        self._plotPDF(X,δ,conditions,m,other_name,other_δ)
        plt.show()
        plt.close()

    def _plotPDF(self,X:RandomVariable,δ=0.05,conditions=None,m=None,other_name=None,other_δ=None):
        if conditions:
            if not other_name:
                other_name = X.name
            rv = util.rvs[other_name][0]
            for c in conditions:
                if other_δ:
                    d = other_δ
                else:
                    d = δ
                    self._plotPDF(rv(*c),δ=d,m=m)
        x, y = [],[]
        m1,m2 = X.getMin(),X.getMax()
        if not m:
            m = m2
        MAX = 200
        i = 0
        if not X.strictLower:
            m1 += δ
        while m1 <= m and i <= MAX:
            x.append(m1)
            y.append(X.pdf(m1))
            print(x[-1],y[-1])
            m1+=δ
            i+=1
        plt.plot(x, y, label=f'{"PMF" if X.isDiscrete() else "PDF"} of {X}')

if __name__ == '__main__':
    P = Plot()
    # P.plotPDF(Binomial(1000,.01),1,conditions=[(10,)],m=30,other_name='poisson')
    P.plotPDF(Binomial(3000,.00333333),1,conditions=[(10,)],m=30,other_name='poisson')

    # P.plotPDF(Poisson(10),.05,m=30)
    # P.plotPDF(Exponential(10),δ=0.01,m=1)
    # P.plotPDF(Binomial(20,.7),1)