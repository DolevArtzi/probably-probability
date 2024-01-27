from player import Player
from random import shuffle

class Table:
    def __init__(self,n=4):
        self.n = n
        self.players = [Player(str(i)) for i in range(n)]
        self.cards = list(range(1,53))
        self.suits = ['club','spade','diamond','heart']
        self.card_names = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
        self.round = 0
        self.last = 0
        self.table = []
        self._inject = False
        self._injected_cot = []
        self._injected_hands = []

    def deal(self):
        if self.n > 26:
            return
        shuffle(self.cards)
        if self._inject:
            t = 0
            # print(self._injected_cot)
            for c in self._injected_cot:
                # print(c,self.cards)
                self.cards.remove(c)
                self.cards.insert(0,c)
                t += 1
            for i,(x,y) in enumerate(self._injected_hands):
                self.players[i].setHand((x,y))
                for c in (x,y):
                    self.cards.remove(c)
                    self.cards.insert(0,c)
                    t += 1
            self.last = t
            # for i,h in enumerate(self._injected_hands):
            #     self.players[i].setHand(h)
            #     for x in h:
            #         self.cards.remove(x)
            #         self.cards.insert(0,x)
            #     self.last += 2
            if len(self._injected_hands) < self.n:
                for p in self.players[len(self._injected_hands):]: 
                    x,y = self.cards[self.last],self.cards[self.last+1]
                    self.last += 2
                    p.setHand((x,y))
        else:
            for p in self.players:
                x,y = self.cards[self.last],self.cards[self.last+1]
                self.last += 2
                p.setHand((x,y))

    """
    cards are represented by 1-52. 1-13 are clubs, with 1 being Ace and 13 being King. The pattern continues according
    to the ordering in self.suits
    """
    def cardName(self,card):
        suit = (card-1)//13
        idx = (card-1) % 13
        return f'{self.card_names[idx]} of {self.suits[suit]}s'


    def printHand(self,p,ret=False,retCards=False):
        s = '('
        for c in p.getHand():
            s += self.cardName(c) + ', '
        s = s[:-2] + ')'
        x = f'Player {p.name}: {s}'
        if retCards:
            return s
        if ret:
            return x
        else:
            print(x) 

    def reset(self):
        self._inject = False
        self._injected_cot = []
        self._injected_hands = []
        for i in range(self.n):
            self.players[i].setHand(())
        self.round = 0
        self.last = 0
        self.table = []

    def open(self,k):
        if self._inject:
            if k == 3:
                for i in range(k):
                    c = self._injected_cot[i]
                    self.table.append(c)
                    self.cards.remove(c)
                    self.cards.insert(0,c)
                    self.last += 1
            elif len(self.table) >= len(self._injected_cot): # didn't provide a full injected table
                self.table.append(self.cards[self.last])
                self.last += 1
            else:
                # gets the fourth card in self._injected_cot if we're on the turn, the fifth if the river
                # print(k,self.table,self._injected_cot,self.cards,self.last)
                c = self._injected_cot[len(self.table)]
                self.table.append(c)
                self.cards.remove(c)
                self.cards.insert(0,c)
                self.last += 1
        else:
            for j in range(k):
                self.table.append(self.cards[self.last])
                self.last += 1

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

    def printTable(self):
        s = self.printCards(self.table,ret=True)
        print(f'Open Cards: {s}')

    def getCardsOnTable(self):
        return self.table

    def inject(self,cots,hands):
        self._inject = True
        self._injected_cot = cots
        self._injected_hands = hands

if __name__ == '__main__':
    t = Table()
    for i in t.cards:
        print(t.cardName(i))