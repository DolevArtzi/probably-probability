from table import Table
from eval import Eval
from display import TableDisplay
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

    def start(self,statMode=False,_print=True,_display=False,_sort=True):
        self.t.reset()
        self.t.deal()
        self.t.progress()
        self.t.progress()
        self.t.progress()
        if not statMode:
            if _print:
                self.t.printTable()
            if _display:
                open_cards = self.t.printCards(self.t.table,ret=True)
                self.disp.split_display(open_cards,w=90)
            best_hands = []
            cards = []
            for p in self.t.players:
                x = self.e.evaluate(p,self.t)
                if _display:
                    cards.append(self.t.printHand(p,retCards=True))
                    # self.disp.displayHand(^,w=65)
                    print(f'Player {p}: ({self.e.strength[x[0]]})')
                    l = x[-1]
                    if _sort:
                        best_hand = self.e.sortHand(l)
                    else:
                        best_hand = l
                    best_hands.append(best_hand)
                    # self.disp.split_display(self.t.printCards(best_hand,ret=True),w=70)
            for i in range(len(best_hands)):
                best_hands[i] = self.t.printCards(best_hands[i],ret=True)
            if _display:
                cards = [''.join((list(c)[1:])[:-1]).split(',') for c in cards]
                # for c in cards:

        #                     h = handString
        # h = list(h)
        # h = h[1:]
        # h = h[:-1]
        # l = ''.join(h).split(',')
                self.disp.display_all_hands(cards)
                self.disp.display_all_hands(best_hands)
        else:
            return self.e.evaluate(self.t.players[0],self.t)

if __name__ == '__main__':
    g = Game()
