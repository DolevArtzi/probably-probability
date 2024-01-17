from table import Table
from math import perm
from collections import Counter
import itertools
from player import Player
import random

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
        values: (f,argIdxs) where f is a function that determines whether a given hand has achieved the strength
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
        if 0 in sortedA:
            return sortedA == [0,1,2,3,4] or sortedA == [0,9,10,11,12]
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

    """
    add docs. retKeys assumes len(seq) == 2
    """
    def _sequence(self,cards,seq,retKeys=False):
        t,k = self.blankOfAKind(cards,seq[0],ret=True)
        if t:
            if retKeys:
                t2,k2 = self.blankOfAKind(cards,seq[1],exclude=[k],ret=True)
                return k,k2
            return self.blankOfAKind(cards,seq[1],exclude=[k])
        return False

    def fullHouse(self,cards,retKeys=False):
        return self._sequence(cards,[3,2],retKeys=retKeys)

    def twoPair(self,cards,retKeys=False):
        return self._sequence(cards,[2,2],retKeys=retKeys)

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

    def _shortCircuitImprove(self,cards,suits,best_score,best_hand=None,report=False):
        if not best_hand:
            best_hand = cards[:]
        args = [cards[:],suits[:],2,3,4]
        for score in range(self.MAXSCORE,-1,-1):
            if score < best_score:
                if report:
                    return best_score,best_hand,False
                return best_score,best_hand
            else:
                f,argIdxs = self._getInfoFromScore(score)
                if f(*[args[i] for i in argIdxs]):
                    if score == best_score:
                        o = self._compareHands(cards, best_hand, best_score)
                        if report:
                            return (score, cards,True) if o == GREATER else (best_score, best_hand,False)
                        return (score, cards) if o == GREATER else (best_score, best_hand)
                    if report:
                        return score,cards,True
        if report:
            return best_score,best_hand,False
        return best_score,best_hand

    def _getCombos(self,player,t):
        hand = player.getHand()
        if t:
            cards_on_table = t.getCardsOnTable()
            cards = cards_on_table[:]
            cards.extend(list(hand))
        else:
            cards = hand
        choices = [list(pair) for pair in itertools.combinations(cards,5)]
        return choices

    # def _getScore(hand):
    
    def evaluate(self,player,t,getHand=False):
        choices = self._getCombos(player=player,t=t)
        best_score = 0
        best_hand = None
        best_hand_idx = 0
        for i, choice in enumerate(choices):
            suits = [self.getSuit(c) for c in choice] #order matters between this and the next line. document that.
            realChoice = [self.getCard(c) for c in choice]
            best_score, best_hand, isBetter = \
                self._shortCircuitImprove(realChoice,suits,best_score,best_hand,report=True)
            if isBetter:
                best_hand_idx = i
        if t:
            print(f'{t.printHand(player,ret=True)}: {self.strength[best_score]}; {t.printCards(choices[best_hand_idx],ret=True)}')
            return self.strength[best_score] \
                       if not getHand \
                       else self.strength[best_score],t.printCards(choices[best_hand_idx],ret=True)
        return self.strength[best_score] if not getHand else self.strength[best_score], best_hand

    """
    Compares cards c1 and c2
    :returns ORD
    
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
        if c1 == 0: #check for Aces
            return GREATER
        if c2 == 0:
            return LESS
        if c1 < c2:
            return LESS
        return GREATER

    def _compareStraight(self,h1,h2):
        return self._compMax(h1,h2)

    def _compMax(self,h1,h2):
        x1,x2 = 1 if 1 in h1 else max(h1), 1 if 1 in h2 else max(h2)
        return self.compare(x1,x2)

    def _compareKOfAKind(self,h1,h2,score):
        if score == 1: #pair
            k = 2
        elif score == 3: #3oak
            k = 3
        elif score == 7: #4oak
            k = 4
        (_,val1),(_,val2) = self.blankOfAKind(h1,k,ret=True),self.blankOfAKind(h2,k,ret=True)
        return self.compare(val1,val2)

    def _compareSeq(self,h1,h2,score):
        if score == 2: #two pair
            f = self.twoPair
        else:
            f = self.fullHouse
        (k11, k12), (k21, k22) = f(h1,retKeys=True),f(h2,retKeys=True)
        o1 =  self.compare(k11,k21)
        return o1 if o1 != EQUAL else self.compare(k12,k22)

    """
    Compares two five card hands that both fall into the same score class
    ex: the better between two full houses
    :returns: ORD
    
    (order dependent implementation for speed)
    """
    def _compareHands(self,h1,h2,score):
        # print('heaa',h1)
        if score in [0,4,5,8]: #[high card,straight,flush,straight flush] (NOTE: dependent on ordering)
            return self._compareStraight(h1,h2)
        elif score in [1,3,7]:
            return self._compareKOfAKind(h1,h2,score)
        else:
            return self._compareSeq(h1,h2,score)

    """
    for use in self.sortHands, assumes h1 and h2 are (hand,id) tuples
    """
    def _compareHandsTuple(self,h1,h2,score):
        return self._compareHands(h1[0],h2[0],score)

    def _printOrd(self,o):
        print(ord[o])

    def _getHandScore(self,hand):
        suits = [self.getSuit(c) for c in hand]
        hand = [self.getCard(c) for c in hand]

        if self.isStraightFlush(hand,suits):
            return 8
        if self.blankOfAKind(hand,4):
            return 7
        if self.fullHouse(hand):
            return 6
        if self.isFlush(suits):
            return 5
        if self.isStraight(hand):
            return 4
        if self.blankOfAKind(hand,3):
            return 3
        if self.twoPair(hand):
            return 2
        if self.blankOfAKind(hand,2):
            return 1 
        return 0

    def _sortHands(self,p,t):
        c = self._getCombos(p,t)
        m = {i:[] for i in range(self.MAXSCORE+1)}
        id = 0
        id_map = []
        for h in c:
            id_map.append(h)
            m[self._getHandScore(h)].append((h,id))
            id+=1
        final = []
        for score in range(self.MAXSCORE,-1,-1):
            arr = m[score]
            print('arr',arr)
            for i in range(len(arr)):
                hand,h_id = arr[i]
                hand = [self.getCard(c) for c in hand]
                arr[i] = (hand,h_id)
            sorted_score = self._quicksort(arr,score)
            for s in sorted_score:
                final.append(s)
        return final,id_map
    
    def sortHands(self,p,t):
        f,id_map = self._sortHands(p,t)
        final = []
        for h in f:
            raw_h = id_map[h[1]]
            final.append(raw_h)
        return final


        

    def _quicksort(self,a,score):
        x = 1
        if len(a) <= 1:
            return a
        pivot = random.choice(a)
        less = [x for x in a if self._compareHandsTuple(x,pivot,score) == LESS]
        equal = [x for x in a if self._compareHandsTuple(x,pivot,score) == EQUAL]
        greater = [x for x in a if self._compareHandsTuple(x,pivot,score) == GREATER]
        sorted_less, sorted_greater = self._quicksort(less,score),self._quicksort(greater,score)
        return sorted_less + equal + sorted_greater



if __name__ == '__main__':
    e = Eval()
    t = Table()
    p = Player('hi')
    p.setHand([9,10,11,1,12])
    print(e.evaluate(p,None))