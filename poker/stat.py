from game import Game
from eval import Eval
from matplotlib import pyplot as plt
from table import Table
from time import perf_counter
from plot import Plot
class PokerStat:
    def iterate(self,k,show=True):
        g = Game(n=1,statMode=True)
        strength = ['high card','pair','two pair','3 of a kind','straight','flush','full house','4 of a kind','straight flush']

        m = {x:0 for x in strength}
        for _ in range(k):
            outcome = g.start(statMode=True)
            m[outcome]+=1
        ys = []
        for x in strength:
            ys.append(m[x])
        if show:
            plt.bar(strength,[y/k for y in ys],width=.7,color='blue')
            plt.xlabel('Hand Strength')
            plt.ylabel('Percentage of Occurrences')
            plt.title(f'Hand Strength for {k} Random Poker Hands')
            plt.show()
            plt.close()
            print(m)

    def timeIt(self):
        p = Plot()
        m = {
            'f': self._timeIters,
            'mn': 0,
            'mx': 5000,
            'δ': 200,
            'lobf': True
        }
        chart = {
            'xlabel': f'Number of hands played, k',
            'ylabel': f'Time (seconds)',
            'title': f'Time vs. #Hands Played for up to {m["mx"]} Hands',
        }
        p.plotGeneric(fInfo=m, chart=chart, addStats=False)

    def _timeIters(self,k):
        tic = perf_counter()
        S.iterate(k,show=False)
        toc = perf_counter()
        return toc - tic


if __name__ == '__main__':
    S = PokerStat()
    S.timeIt()