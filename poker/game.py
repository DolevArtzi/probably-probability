from table import Table
from eval import Eval
from display import TableDisplay
'''
Class that controls the flow of the game
'''
class Game:
    def __init__(self,n=2,t=None,statMode=False):
        self.t = Table(n=n) if not t else t
        self.e = Eval()
        self.disp = TableDisplay()

        if not statMode:
            self.start()

    def start(self,statMode=False,_print=True):
        self.t.reset()
        self.t.deal()
        self.t.progress()
        self.t.progress()
        self.t.progress()
        if not statMode:
            if _print:
                # self.t.printTable()
                open_cards = self.t.printCards(self.t.table,ret=True)
                print('--->',open_cards)
                self.disp.split_display(open_cards)
                # self.disp.display([])
            for p in self.t.players:
                x = self.e.evaluate(p,self.t)
                # self.disp.split_display(self.t.players)
                self.disp.split_display(x[-1])
        else:
            return self.e.evaluate(self.t.players[0],self.t)


if __name__ == '__main__':
    g = Game()
