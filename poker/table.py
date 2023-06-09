from player import Player
from random import shuffle

class Table:
    def __init__(self,n=4):
        self.n = n
        self.players = [Player(str(i)) for i in range(n)]
        self.cards = list(range(1,53))
        self.suits = ['club','spade','diamond','heart']
        self.card_names = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
        self.active = [True for _ in range(n)]
        self.round = 0
        self.last = -1
        self.table = []

    def deal(self):
        if self.n > 26:
            return
        shuffle(self.cards)
        i = 0
        for p in self.players:
            x,y = self.cards[i],self.cards[i+1]
            i+=2
            p.setHand((x,y))
        self.last = i

    def cardName(self,card):
        suit = (card-1)//13
        idx = (card-1) % 13
        return f'{self.card_names[idx]} of {self.suits[suit]}s'

    def printHand(self,p,ret=False):
        s = '('
        for c in p.getHand():
            s += self.cardName(c) + ', '
        s = s[:-2] + ')'
        x = f'Player {p.name}: {s}'
        if ret:
            return x
        else:
            print(x)

    def reset(self):
        for i in range(self.n):
            self.active[i] = True
            self.players[i].setHand(())
        self.round = 0
        self.last = -1
        self.table = []

    def open(self,k):
        for j in range(k):
            self.table.append(self.cards[self.last])
            self.last+=1

    def progress(self):
        if self.round == 0:
            self.open(3)
        else:
            self.open(1)
        self.round+=1

    def printCards(self,cards=None,ret=False):
        if not cards:
            cards = self.cards
        r = [self.cardName(c) for c in cards]
        if ret:
            return r
        print(r)

    def printTable(self):
        s = self.printCards(self.table,ret=True)
        print(f'Open Cards: {s}')

    def getCardsOnTable(self):
        return self.table

if __name__ == '__main__':
    t = Table()
    for i in t.cards:
        print(t.cardName(i))