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

    def start(self,statMode=False,_print=True,_display=False):
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
                self.disp.split_display(open_cards)
            for p in [self.t.players[0]]:
                x = self.e.evaluate(p,self.t)
                if _display:
                    self.disp.displayHand(self.t.printHand(p,retCards=True))
                    if _print:
                        print(f'Player {p}: ({self.e.strength[x[0]]}) {self.t.printCards(x[1],ret=True)}')
                    self.disp.split_display(self.t.printCards(x[-1],ret=True))
        else:
            return self.e.evaluate(self.t.players[0],self.t)


if __name__ == '__main__':
    g = Game()
