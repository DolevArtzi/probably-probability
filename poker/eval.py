from table import Table
from math import perm
from collections import Counter
import itertools
class Eval:
    def __init__(self):
        self.strength = ['high card','pair','two pair','3 of a kind','straight','flush','full house','4 of a kind','straight flush']

    def getSuit(self,card):
        return (card-1)//13

    def getCard(self,card):
        return (card-1)%13

    def isStraight(self,cards):
        sortedA = sorted(cards)
        if 1 in sortedA:
            return sortedA == [1,2,3,4,5] or sortedA == [10,11,12,13,1]
        for i in range(len(sortedA)-1):
            if sortedA[i] + 1 != sortedA[i+1]:
                return False
        return True

    def _sequence(self,cards,seq):
        t,k = self.blankOfAKind(cards,seq[0],ret=True)
        if t:
            return self.blankOfAKind(cards,seq[1],exclude=[k])
        return False

    def fullHouse(self,cards):
        return self._sequence(cards,[3,2])

    def twoPair(self,cards):
        return self._sequence(cards,[2,2])

    def blankOfAKind(self,cards,k,exclude=[],ret=False):
        c = Counter(cards)
        for e in exclude:
            c[e] = 0
        for key,v in c.items():
            if v >= k:
                if ret:
                    return True,key
                return True
        if ret:
            return False,None
        return False


    def evaluate(self,player,t):
        hand = player.getHand()
        if t:
            cards_on_table = t.getCardsOnTable()
            cards = cards_on_table[:]
            cards.extend(list(hand))
        else:
            cards = hand
        choices = [list(pair) for pair in itertools.combinations(cards,5)]
        best = 0
        for choice in choices:
            suits = [self.getSuit(c) for c in choice]
            choice = [self.getCard(c) for c in choice]
            s0 = suits[0]
            flush = True
            for s in suits:
                if s0 != s:
                    flush = False
                    break
            # print(suits)
            straight = self.isStraight(choice)
            if flush and straight:
                return self.strength[-1]
            elif self.blankOfAKind(choice,4):
                best = max(best,7)
                continue
            elif self.fullHouse(choice):
                best = max(best,6)
                continue
            elif flush:
                best = max(best,5)
                continue
            elif straight:
                best = max(best,4)
                continue
            elif self.blankOfAKind(choice,3):
                best = max(best,3)
                continue
            elif self.twoPair(choice):
                best = max(best,2)
            elif self.blankOfAKind(choice,2):
                best = max(best,1)
                continue
            else:
                best = max(best,0)
        print(f'{t.printHand(player,ret=True)}: {self.strength[best]}')
        return self.strength[best]


if __name__ == '__main__':
    cards = [4,4,1,4,4]
    e = Eval()
    print(e.twoPair([3,3,1,1,1]))