from plot import Plot
from abc import abstractmethod

class RandomWalk:
    @abstractmethod
    def walk(self,k,j=1,verbose=True,giveVals=False):
        pass

    """
    Visualize num_walks random walks on top of each other
    """
    def graphWalks(self,k,num_walks):
        P = Plot()
        for _ in range(num_walks):
            xs,ys = self.walk(k,verbose=False,giveVals=True)
            P.plotGeneric(data=(xs,ys),wait=True)
        chart = {
            'xlabel': f'Time t, 0 <= t <= {k}',
            'ylabel': f'Value of Random Walk',
            'title': f'Time vs. Value for {num_walks} {k}-Bounded Random Walks', #pass in the title? for each type
        }
        P.fillInChartInfo(chart,show=True)