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
        self.mapStrengths = {x:i for i,x in enumerate(self.strength)} # name --> strength map

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
        args = [cards[:],suits[:],2,3,4] #2,3,4 are there for use by pair, set, and 4oak respectively
        for score in range(self.MAXSCORE,-1,-1):
            if score < best_score:
                if report:
                    return best_score,best_hand,False
                return best_score,best_hand
            else:
                f,argIdxs = self._getInfoFromScore(score)
                if f(*[args[i] for i in argIdxs]):
                    if score == best_score:
                        # if 0 in cards or 0 in best_hand:
                        #     print('beware THE ZEROOOO!!!!!')
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
    
    def evaluate(self,player,t):
        choices = self._getCombos(player=player,t=t)
        # print('choices',choices)
        scores = [(hand,self._getHandScore(hand)) for hand in choices]
        max_score = max(scores,key=lambda x:x[1])[1]
        top = [hand for (hand,score) in scores if score == max_score]
        sorted_score, id_map = self._sortScoreClass(top,max_score)
        # print(sorted_score)
        # print(id_map)
        best_hand = id_map[sorted_score[-1][1]]
        # print('best hand',best_hand)
        for x in sorted_score:
            print(x)
        # print(f'{t.printHand(player,ret=True)}: {self.strength[max_score]}; {t.printCards(choices[best_hand_idx],ret=True)}')
        
        return max_score,best_hand
        # best_score = 0
        # best_hand = None
        # best_hand_idx = 0
        # for i, choice in enumerate(choices):
        #     suits = [self.getSuit(c) for c in choice] 
        #     realChoice = [self.getCard(c) for c in choice] #1-52 --> 0-12
        #     best_score, best_hand, isBetter = \
        #         self._shortCircuitImprove(realChoice[:],suits,best_score,best_hand,report=True)
        #     # print('best',best_hand)
        #     if isBetter:
        #         best_hand_idx = i
        # if t:
        #     return self.strength[best_score] \
        #                if not getHand \
        #                else self.strength[best_score],t.printCards(choices[best_hand_idx],ret=True)
        # return self.strength[best_score] if not getHand else self.strength[best_score], best_hand

    """
    Compares cards c1 and c2
    :returns ORD
    
    if c1 < c2: returns LESS
    elif c1 == c2: returns EQUAL
    else: GREATER
    
    """
    def compare(self,c1,c2,get=False):
        # if not get:
        #     c1 = self.getCard(c1)
        #     c2 = self.getCard(c2)
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


    # def _compMax(self,h1,h2):
    #     if 0 in h1 or 0 in h2:
    #         print('0 is HEREEEEEE!!!!!')
    #     x1,x2 = 0 if 0 in h1 else max(h1), 0 if 0 in h2 else max(h2)
    #     return self.compare(x1,x2)

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
        if len(seq1) != len(seq2):
            print('unequal lengths', seq1,seq2)
        # print('TOP',seq1,seq2,order)
        # print(self._getHandScore(seq1),self._getHandScore(seq2),'SCORE')
        if seq1 == seq2:
            return EQUAL
        if seq1 == seq2 == []:
            # print('in empty cmp prec.')
            return EQUAL
        if not len(order[0]) and not len(order[1]):
            order = 'all'
        if order == 'all':
            # print('before seq1m1', seq1)
            m1,m2 = self._takeTop(seq1), self._takeTop(seq2)
            # print(seq1,m1,'seq1 m1')
            o = self.compare(m1,m2)
            # print('o--->',o,m1,m2)
            if o != EQUAL:
                return o
            seq1.remove(m1)
            seq2.remove(m2)
            return self._compareWithPrecedence(seq1,seq2,order='all')
        else:
            if len(order[0]) != len(order[1]):
                print(order,'UNEQUAL ORDER')
            #e.g order = ([(v1_1,k1_1),(v1_2,k1_2),(v1_3,k1_3)], [(v2_1,k2_1),(v2_2,k2_2),(v2_3,k2_3)])
            v1,k1 = order[0][0]
            v2,k2 = order[1][0]
            # print('v1,v2',v1,v2,k1,k2,order,seq1,seq2)
            if k1 != k2:
                print('BUG') #can be deleted before committing
            o = self.compare(v1,v2)
            if o != EQUAL:
                return o
            for _ in range(k1):
                seq1.remove(v1)
                seq2.remove(v2)
            return self._compareWithPrecedence(seq1,seq2,(order[0][1:],order[1][1:]))

    def  _compareKOfAKind(self,h1,h2,score):
        # print(h1,h2,'top of compare k of a kind')
        if score == 1: #pair
            k = 2
        elif score == 3: #3oak
            k = 3
        elif score == 7: #4oak
            k = 4
        (_,val1),(_,val2) = self.blankOfAKind(h1,k,ret=True),self.blankOfAKind(h2,k,ret=True)
        # print('val1,val2 in compare k of a kind',val1,val2,h1,h2,k)
        # o = self.compare(val1,val2)
        # if o != EQUAL:
        #     return o
        # for _ in range(k):
        #     h1.remove(val1)
        #     h2.remove(val2)
        return self._compareWithPrecedence(h1,h2,order=([(val1,k)], [(val2,k)]))
        # if val1 == val2, then we need to compare the rest of the hand
        # this can be done by removing k copies of the number and then taking the highest 5 - k 
        # remaining cards available
        return self.compare(val1,val2)

    def _compareSeq(self,h1,h2,score):
        if score == 2: #two pair
            f = self.twoPair
        else:
            f = self.fullHouse
        # print('in compare seq',score,h1,h2)
        (v11, v12), (v21, v22) = f(h1,retKeys=True),f(h2,retKeys=True)
        # print(h1,h2,score,v11,v12)
        k12, k22 = 2,2
        if score == 2:
            k11,k21 = 2,2
        else:
            k11,k21 = 3,3
        order = ([(v11,k11),(v12,k12)],[(v21,k21),(v22,k22)])
        # print('hello',order)
        if score == 2:
            # print('here')
            if self.compare(v11,v12) == LESS:
                o0 = [(v12,k12),(v11,k11)]
                order = (o0,order[1])
            if self.compare(v21,v22) == LESS:
                o1 = [(v22,k22),(v21,k21)]
                order = (order[0],o1)
            
        # print('val1,val2 in compareseq',v11,v12,v21,v22)
        return self._compareWithPrecedence(h1,h2,order=order)
        # o1 =  self.compare(v11,v21)
        # if o1 != EQUAL:
        #     return o1
        # o2 = self.compare(v12,v22)
        # if o2 != EQUAL:
        #     return o2
        

    """
    Compares two five card hands that both fall into the same score class
    ex: the better between two full houses
    :returns: ORD
    
    (order dependent implementation for speed)



    straight or straight flush: top card
    everything else: highest possible across all cards: eg AAQQJ > AAQQ7, 66442 > 5544A
    """
    def _compareHands(self,h1,h2,score):
        # print('heaa',h1)

        if score in [0,5]: #[high card, flush]
            return self._compareWithPrecedence(h1,h2,order='all')
        if score in [4,8]: #[straight, straight flush] (NOTE: dependent on ordering)
            return self._compareStraight(h1,h2)
        elif score in [1,3,7]: #[pair, set, four of a kind]
            return self._compareKOfAKind(h1,h2,score)
        else: #[two pair, full house]
            # print(h1,h2,'in compare hands')
            return self._compareSeq(h1,h2,score)

    """
    for use in self.sortHands, assumes h1 and h2 are (hand,id) tuples
    """
    def _compareHandsTuple(self,h1,h2,score):
        # print('compare',h1,h2)
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
    sorts the hands in `l`, which are all in the score class `score`, and returns 
    (sorted_score,id_map) where sorted_score[i] is (0-12 hand,id) and id_map[id] = 1-52 hand corresponding to the 0-12 hand
    sorted_score[-1] is the best hand
    
    """
    def _sortScoreClass(self,l,score):
        id = 0
        id_map = []
        arr = []
        for h in l:
            id_map.append(h)
            arr.append((h,id))
            id+=1
        for i in range(len(arr)):
            hand,h_id = arr[i]
            hand = [self.getCard(c) for c in hand]
            arr[i] = (hand,h_id)
        sorted_score = self._quicksort(arr,score)
        return sorted_score,id_map


    # def _sortHands(self,p,t):
    #     c = self._getCombos(p,t)
    #     m = {i:[] for i in range(self.MAXSCORE+1)}
    #     id = 0
    #     id_map = []
    #     for h in c:
    #         id_map.append(h)
    #         m[self._getHandScore(h)].append((h,id))
    #         id+=1
    #     final = []
    #     for score in range(self.MAXSCORE,-1,-1):
    #         arr = m[score]
    #         for i in range(len(arr)):
    #             hand,h_id = arr[i]
    #             hand = [self.getCard(c) for c in hand]
    #             arr[i] = (hand,h_id)
    #         sorted_score = self._quicksort(arr,score)
    #         for s in sorted_score:
    #             final.append(s)
    #     return final,id_map
    
    # def sortHands(self,p,t):

    # def sortHands(self,p,t):
    #     f,id_map = self._sortHands(p,t)
    #     final = []
    #     for h in f:
    #         raw_h = id_map[h[1]]
    #         final.append(raw_h)
    #     return final

    def _quicksort(self,a,score):
        # print('arrrrrr',a)
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