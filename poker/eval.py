from table import Table
from math import perm
from collections import Counter
import itertools
from player import Player
import random


comb = itertools.combinations
prod = itertools.product
chain = itertools.chain
COMB = 'comb'
PROD = 'prod'
CHAIN = 'chain'
COMBPROD = 'combprod'
from combiner import Combiner
from sorter import Sorter

LESS = 0
EQUAL = 1
GREATER = 2
ord = {0:'LESS',1:'EQUAL',2:'GREATER'}

class Eval:
    def __init__(self):
        self.strength = ['high card','pair','two pair','3 of a kind','straight','flush','full house','4 of a kind','straight flush']
        self.mapStrengths = {x:i for i,x in enumerate(self.strength)} # name --> strength map
        self.c = Combiner()
        self.s = Sorter(cmp_fxs=[self._compareHandsTuple,self.compare,self._compareHands])

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

    '''
    Assumes post-river
    '''
    def _getCombos(self,player,t):
        hand = player.getHand()
        if t:
            cards_on_table = t.getCardsOnTable()
            cards = cards_on_table[:]
            cards.extend(list(hand))
        else:
            cards = hand
        choices = [list(pair) for pair in comb(cards,5)]
        return choices
        
    def evaluate(self,player,t,choices=None):
        choices = choices if choices else self._getCombos(player=player,t=t)
        scores = [(hand,self._getHandScore(hand)) for hand in choices]
        max_score = max(scores,key=lambda x:x[1])[1]
        top = [hand for (hand,score) in scores if score == max_score]
        sorted_score, id_map = self.s._sortScoreClass(top,max_score)
        best_hand = id_map[sorted_score[-1][1]]       
        return max_score,best_hand

    """
    Compares cards c1 and c2
    :returns ORD
    
    if c1 < c2: returns LESS
    elif c1 == c2: returns EQUAL
    else: GREATER
    
    """
    def compare(self,c1,c2):
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
        x1 = 0 if 0 in h1 and 1 not in h1 else max(h1) #ace if straight to the ace, not to the 5
        x2 = 0 if 0 in h2 and 1 not in h2 else max(h2)
        return self.compare(x1,x2)

    """
    selects the highest card from the list `cards`
    """
    def _takeTop(self,cards):
        m = 0 if 0 in cards else max(cards)
        return m

    '''
    compares hands according to a specified ordering. 

    :param: order: either 'all' or a pair of ordered lists of v,k tuples
        - if 'all': the hands will be compared, each time comparing the next highest cards in each seq1 and seq2
        - if (vk1,vk2) then vk1 is an ordered list of (card #, k) pairs where the card # is that of e.g. the first pair in the 
        two pair, and k is 2, in the case of a two pair. 

        e.g.: in a two pair, you first compare the top pair, then the next pair, then the kicker
    '''
    def _compareWithPrecedence(self,seq1,seq2,order='all'):
        seq1 = seq1[:]
        seq2 = seq2[:]
        if seq1 == seq2:
            return EQUAL
        if seq1 == seq2 == []:
            return EQUAL
        if not len(order[0]) and not len(order[1]):
            order = 'all'
        if order == 'all':
            m1,m2 = self._takeTop(seq1), self._takeTop(seq2)
            o = self.compare(m1,m2)
            if o != EQUAL:
                return o
            seq1.remove(m1)
            seq2.remove(m2)
            return self._compareWithPrecedence(seq1,seq2,order='all')
        else:
            v1,k1 = order[0][0]
            v2,_ = order[1][0]
            o = self.compare(v1,v2)
            if o != EQUAL:
                return o
            for _ in range(k1):
                seq1.remove(v1)
                seq2.remove(v2)
            return self._compareWithPrecedence(seq1,seq2,(order[0][1:],order[1][1:]))

    def  _compareKOfAKind(self,h1,h2,score):
        if score == 1: #pair
            k = 2
        elif score == 3: #3oak
            k = 3
        elif score == 7: #4oak
            k = 4
        (_,val1),(_,val2) = self.blankOfAKind(h1,k,ret=True),self.blankOfAKind(h2,k,ret=True)
        return self._compareWithPrecedence(h1,h2,order=([(val1,k)], [(val2,k)]))

    def _compareSeq(self,h1,h2,score):
        if score == 2: #two pair
            f = self.twoPair
        else:
            f = self.fullHouse
        (v11, v12), (v21, v22) = f(h1,retKeys=True),f(h2,retKeys=True)
        k12, k22 = 2,2
        if score == 2:
            k11,k21 = 2,2
        else:
            k11,k21 = 3,3
        order = ([(v11,k11),(v12,k12)],[(v21,k21),(v22,k22)])
        if score == 2:
            if self.compare(v11,v12) == LESS:
                o0 = [(v12,k12),(v11,k11)]
                order = (o0,order[1])
            if self.compare(v21,v22) == LESS:
                o1 = [(v22,k22),(v21,k21)]
                order = (order[0],o1)            
        return self._compareWithPrecedence(h1,h2,order=order)

    """
    Compares two five card hands that both fall into the same score class
    ex: the better between two full houses

    NOTE: expects the hands to be 0-12, not 1-52

    :returns: ORD
    """
    def _compareHands(self,h1,h2,score):
        if score in [0,5]: #[high card, flush]
            return self._compareWithPrecedence(h1,h2,order='all')
        if score in [4,8]: #[straight, straight flush] (NOTE: dependent on ordering)
            return self._compareStraight(h1,h2)
        elif score in [1,3,7]: #[pair, set, four of a kind]
            return self._compareKOfAKind(h1,h2,score)
        else: #[two pair, full house]
            return self._compareSeq(h1,h2,score)

    """
    assumes h1 and h2 are (hand,id) tuples
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

    """
    Determines the winners of the round, given each player's best five card hand and that hand's score
    :param: best_hands: the best hand for each player, in order
    :param: scores: the score for each player, in order
    :returns: list of indices into best_hands, all of whom tie for winner (or 1 winner)
    """
    def determineWinner(self,best_hands,scores):
        m = max(scores)
        top =  [i for i in range(len(scores)) if scores[i] == m]
        if len(top) == 1:
            return top
        sorted_player_hands, id_map = self.s._sortScoreClass(best_hands[:],m)

        winner_hand = id_map[sorted_player_hands[-1][1]]
        winner_idx = best_hands.index(winner_hand)
        winners = []
        for top_idx in top:
            if self._compareHands([self.getCard(c) for c in best_hands[top_idx]],[self.getCard(c) for c in best_hands[winner_idx]],m) == EQUAL:
                winners.append(top_idx)
        return winners

    def classProbabilities(self,possible_hands):
        print(len(possible_hands),'classProb.')
        m = {i:0 for i in range(len(self.strength))}
        tot = 0
        for h in possible_hands:
            m[self._getHandScore(h)] += 1
            tot += 1
        if tot == 0:
            print(possible_hands,'hello')
        for k in m:
            m[k] *= 100 / tot
        return m
    
    def probOfImprovement(self,possible_hands,p:Player,t:Table):
        # print(len(possible_hands),'classProb.2')
        m = {i:0 for i in range(len(self.strength))}
        tot = 0
        guaranteed_hands = self.c.getGuaranteedHands(p,t)

        best_score,best_hand = self.evaluate(-1,-1,choices=guaranteed_hands[:])
        if len(t.getCardsOnTable()) == 5:
            return self.strength[best_score], {}
        best_hand = [self.getCard(c) for c in best_hand]
        for h in possible_hands:
            score = self._getHandScore(h)
            if score > best_score:
                m[score] += 1
                tot += 1
            elif score == best_score:
                if self._compareHands(best_hand,[self.getCard(c) for c in h],score) == LESS:
                    m[score] += 1
                    tot += 1
        for k in m:
            m[k] *= 100 / tot
        return self.strength[best_score], {self.strength[k]:m[k] for k in m if m[k] > 0}

    # def classProb2(self,)

    # def bestSoFar(self,possible_hands):
    #     best_score,best_hand = self.evaluate(-1,-1,choices=possible_hands)
    #     return best_score,best_score



if __name__ == '__main__':
    e = Eval()
    t = Table()
    p = Player('hi')
    p.setHand([9,10,11,1,12])
    print(e.evaluate(p,None))