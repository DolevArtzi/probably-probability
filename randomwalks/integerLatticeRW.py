from RandomWalk import RandomWalk
from Bernoulli import Bernoulli
from mathutil import avgVar
class IntegerLatticeRW(RandomWalk):
    def walk(self,k,j=1,verbose=True,giveVals=False):
        if giveVals:
            xs,ys = [],[]
        r = []
        X = Bernoulli(.5)
        for _ in range(j):
            s = [0,0]
            for i in range(k):
                s[0] += 1 if X.genVar() else -1
                s[1] += 1 if X.genVar() else -1
                if giveVals:
                    xs.append(s[0])
                    ys.append(s[1])
            r.append(s)
        if verbose:
            if j == 1:
                print(f'Random Walk Endpoint for {k} iters: {s}')
            else:
                print(f'Random Walk Endpoints for {k} iters: {r}')
                xs,ys = [x for x,y in r],[y for x,y in r]
                avgX,varX = avgVar(xs)
                avgY,varY = avgVar(ys)
                print(f'Sample Average: {(avgX,avgY)}; Sample Variance: {varX,varY} ({j} Samples)')
        if giveVals:
            return xs,ys


if __name__ == '__main__':
    z = IntegerLatticeRW()
    # z.walk(1000,100)
    z.graphWalks2D(200,30)

