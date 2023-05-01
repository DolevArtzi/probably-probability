from game import Game
from eval import Eval
from matplotlib import pyplot as plt
class PokerStat:
    def iterate(self,k):
        g = Game(n=1)
        strength = ['high card','pair','two pair','3 of a kind','straight','flush','full house','4 of a kind','straight flush']

        m = {x:0 for x in strength}
        for _ in range(k):
            outcome = g.start(statMode=True)
            m[outcome]+=1
        ys = []
        for x in strength:
            ys.append(m[x])
        plt.bar(strength,[y/k for y in ys],width=.7,color='blue')
        plt.xlabel('Hand Strength')
        plt.ylabel('Percentage of Occurrences')
        plt.title(f'Hand Strength for {k} Random Poker Hands')
        plt.show()
        plt.close()
        print(m)

if __name__ == '__main__':
    S = PokerStat()
    S.iterate(5000)
