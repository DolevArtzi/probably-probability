from table import Table
from eval import Eval
from display import TableDisplay
from itertools import product,chain


'''
Class that controls the flow of the game
'''
class Game:
    def __init__(self,n=2,t=None,statMode=False,start=True):
        self.t = Table(n=n) if not t else t
        self.e = Eval()
        self.disp = TableDisplay()

        if not statMode and start:
            self.start()

    def start(self,statMode=False,_probMode=True,_print=True,_display=False,_sort=True,_inject=[]):
        self.t.reset()
        if _inject != []:
            injected_hands = []
            if len(_inject) > 2: # not (cot,hands), just cot
                injected_cot = _inject
            else:
                injected_cot, injected_hands = _inject
            self.t.inject(injected_cot,injected_hands)
        self.t.deal()
        # x = self.e.c._getOppCombos(self.t.players[0],self.t)
        # y = self.e.c._getPlayerCombos(self.t.players[0],self.t)
        # l1 = len(x)
        # l2 = len(y)
        # print(self.e.classProbabilities(y))
        # print(l1,l2,l1*l2)

        self.t.progress()
        if _probMode:
            x = self.e.c._getOppCombos(self.t.players[0],self.t)
            y = self.e.c._getPlayerCombos(self.t.players[0],self.t)
            l1 = len(x)
            l2 = len(y)
            # print(self.e.classProbabilities2(y))
            best_score, p, probs = self.e.probOfImprovement(y,self.t.players[0],self.t)
            print(f'Best Guaranteed: {best_score}, Prob. of Improving: {p}')
            m = {k:f'{probs[k]:.6f}' for k in probs}
            print(f'Prob. of Improving to Score Class: {m}')
            # print(l1,l2,l1*l2)
            print()
        self.t.progress()
        if _probMode:
            x = self.e.c._getOppCombos(self.t.players[0],self.t)
            y = self.e.c._getPlayerCombos(self.t.players[0],self.t)
            l1 = len(x)
            l2 = len(y)
            # print(self.e.classProbabilities2(y))
            best_score, p, probs = self.e.probOfImprovement(y,self.t.players[0],self.t)
            print(f'Best Guaranteed: {best_score}, Prob. of Improving: {p}')
            m = {k:f'{probs[k]:.6f}' for k in probs}
            print(f'Prob. of Improving to Score Class: {m}')
            # print(l1,l2,l1*l2)

        self.t.progress()
        if _probMode:
            x = self.e.c._getOppCombos(self.t.players[0],self.t)
            y = self.e.c._getPlayerCombos(self.t.players[0],self.t)
            l1 = len(x)
            l2 = len(y)
            # print(self.e.classProbabilities2(y))
            # best_score, probs = self.e.probOfImprovement(y,self.t.players[0],self.t)
            # print(f'Best Score Guaranteed: {best_score}')        
            # print(l1,l2,l1*l2)
        if not statMode:
            if _print:
                self.t.printTable()
            if _display:
                open_cards = self.t.printCards(self.t.table,ret=True)
                self.disp.split_display(open_cards,w=90)
            best_hands = []
            cards = []
            scores = []
            for p in self.t.players:
                x = self.e.evaluate(p,self.t)
                scores.append(x[0])
                if _display:
                    cards.append(self.t.printHand(p,retCards=True))
                    print(f'Player {p}: {self.e.strength[x[0]]}')
                    l = x[-1]
                    if _sort:
                        best_hand = self.e.s.sortHand(l)
                    else:
                        best_hand = l
                    best_hands.append(best_hand)
            if _print:
                winner_idxs = self.e.determineWinner(best_hands,scores)
                if len(winner_idxs) == 1:
                    print(f'Winner: Player {winner_idxs[0]}')
                else:
                    print(f'Winners: Players {winner_idxs}')
            for i in range(len(best_hands)):
                best_hands[i] = self.t.printCards(best_hands[i],ret=True)
            if _display:
                cards = [''.join((list(c)[1:])[:-1]).split(',') for c in cards]
                self.disp.display_all_hands(cards)
                self.disp.display_all_hands(best_hands)
        else:
            return self.e.evaluate(self.t.players[0],self.t)

if __name__ == '__main__':
    g = Game()