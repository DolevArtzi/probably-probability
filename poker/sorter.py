
LESS = 0
EQUAL = 1
GREATER = 2
ord = {0:'LESS',1:'EQUAL',2:'GREATER'}
import random

class Sorter:
    def __init__(self,cmp_fxs) -> None:
        self.cmp_fxs = cmp_fxs


    def getSuit(self,card):
        return (card-1)//13

    def getCard(self,card):
        return (card-1)%13


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
        sorted_score = self._quicksort(arr,score,cards=False)
        return sorted_score,id_map
        
    '''
    Sort the cards or hands according to 
        - hands: sorts the hands in increasing order of strength
        - cards: sorts the cards in increasing order of strength

    :param a: a list, either of cards (0-12), of hands (0-12), or (hand,id) tuples
    :param score: if > -1, all hands passed must be of the same score class
    :param cards: True if cards are passed, False if hands are passed
    '''
    def _quicksort(self,a,score=-1,cards=True):
        if len(a) <= 1:
            return a
        pivot = random.choice(a)
        if score > -1:
            cmp = self.cmp_fxs[0] # not the cleanest way to do this...
            args = (score,)
        elif cards:
            cmp = self.cmp_fxs[1]
            args = ()
        else:
            cmp = self.cmp_fxs[2]
            args = (score,)
        less = [x for x in a if cmp(x,pivot,*args) == LESS]
        equal = [x for x in a if cmp(x,pivot,*args) == EQUAL]
        greater = [x for x in a if cmp(x,pivot,*args) == GREATER]
        sorted_less, sorted_greater = self._quicksort(less,score=score,cards=cards),self._quicksort(greater,score=score,cards=cards)
        return sorted_less + equal + sorted_greater

    def sortHand(self,hand):
        m = {self.getCard(x):[] for x in hand}
        for x in hand:
            suitless = self.getCard(x)
            m[suitless].append(x)
        suitless_hand = [self.getCard(x) for x in hand]
        sorted = self._quicksort(suitless_hand,-1,cards=True)
        final = []
        for x in sorted:
            take_from = m[x]
            final.append(take_from[0])
            m[x] = m[x][1:]
        z = self.getCard(final[-1])
        if z == 0:
            mods = [self.getCard(c) for c in final]
            if mods == [1,2,3,4,0]:
                last = final[-1]
                final = final[:-1]
                final.insert(0,last)
        return final