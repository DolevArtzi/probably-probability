from table import Table
from math import perm
from collections import Counter
import itertools

LESS = 0
EQUAL = 1
GREATER = 2
ord = {0:'LESS',1:'EQUAL',2:'GREATER'}

class Eval:
    def __init__(self):
        self.strength = ['high card','pair','two pair','3 of a kind','straight','flush','full house','4 of a kind','straight flush']
        self.mapStrengths = {x:i for i,x in enumerate(self.strength)}

        """
        For use in Eval.evaluate
        
        keys: names of the poker hand strengths
        values: (f,argIdxs) where f is a function that determines whether a given hand has acheieved the strength
                described by the key, and argsIdxs is an ordered list of indices into the 'args'
                list in Eval._shortCircuitImprove
        """
        self.info = {'high card':(lambda x:True,[0]), #[0] is arbitrary for high card could be anything
             'pair':(self.blankOfAKind,[0,2]),
             'two pair':(self.twoPair,[0]),
             '3 of a kind':(self.blankOfAKind,[0,3]),
             'straight':(self.isStraight,[0]),
            'flush':(self.isFlush,[1]),
            'full house':(self.fullHouse,[0]),
            '4 of a kind':(self.blankOfAKind,[0,4]),
            'straight flush':(self.isStraightFlush,[0,1])
            }
        self.MAXSCORE = 8

    def _getInfoFromScore(self,score):
        return self.info[self.strength[score]]
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

    def isFlush(self,suits):
        if not suits:
            return False
        s0 = suits[0]
        for s in suits:
            if s0 != s:
                return False
        return True
    def isStraightFlush(self,cards,suits):
        return self.isFlush(suits) and self.isStraight(cards)

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

    def _shortCircuitImprove(self,cards,suits,best_score,best_hand=None):
        if not best_hand:
            best_hand = cards
        args = [cards,suits,2,3,4]
        for score in range(self.MAXSCORE,-1,-1):
            if score <= best_score: #incomplete: will need to improve locally (within the same score). after compareHands
                return best_score,best_hand
            f,argIdxs = self._getInfoFromScore(score)
            # print(f,print(argIdxs,[args[i] for i in argIdxs]))
            if f(*[args[i] for i in argIdxs]):
                return score,cards
        return best_score,best_hand


    def evaluate(self,player,t):
        hand = player.getHand()
        if t:
            cards_on_table = t.getCardsOnTable()
            cards = cards_on_table[:]
            cards.extend(list(hand))
        else:
            cards = hand
        choices = [list(pair) for pair in itertools.combinations(cards,5)]
        best_score = 0
        best_hand = None
        for choice in choices:
            suits = [self.getSuit(c) for c in choice] #order matters between this and the next line. document that.
            realChoice = [self.getCard(c) for c in choice]
            best_score, best_hand = self._shortCircuitImprove(realChoice,suits,best_score,best_hand)
        yo = 'uncomment the line below me'
        # print(f'{t.printHand(player,ret=True)}: {self.strength[best_score]}')
        return self.strength[best_score]

    """
    if c1 < c2: returns LESS
    elif c1 == c2: returns EQUAL
    else: GREATER
    """
    def compare(self,c1,c2,get=False):
        if not get:
            c1 = self.getCard(c1)
            c2 = self.getCard(c2)
        if c1 == c2:
            return EQUAL
        if c1 == 0:
            return GREATER
        if c2 == 0:
            return LESS
        if c1 < c2:
            return LESS
        return GREATER

    def _printOrd(self,o):
        print(ord[o])

if __name__ == '__main__':
    e = Eval()
    t = Table()

    # for c in t.cards[:10]:
    #     for c1 in t.cards[:15]:
    #         print(t.cardName(c),' ? ',t.cardName(c1))
    #         e._printOrd(e.compare(c,c1))
    # print(t.cardName(t.cards[0]),t.cards[0],e.getCard(t.cards[0]))
