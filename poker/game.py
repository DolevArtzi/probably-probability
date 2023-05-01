from table import Table
from eval import Eval
class Game:
    def __init__(self,n=4):
        self.t = Table(n=n)
        self.e = Eval()
        self.start()

    def start(self,statMode=False):
        self.t.reset()
        self.t.deal()
        self.t.progress()
        self.t.progress()
        self.t.progress()
        if not statMode:
            self.t.printTable()
            for p in self.t.players:
                self.e.evaluate(p,self.t)
        else:
            return self.e.evaluate(self.t.players[0],self.t)


if __name__ == '__main__':
    g = Game()

