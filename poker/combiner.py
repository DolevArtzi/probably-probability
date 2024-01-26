import itertools
comb = itertools.combinations
prod = itertools.product
chain = itertools.chain
COMB = 'comb'
PROD = 'prod'
CHAIN = 'chain'
COMBPROD = 'combprod'
COMBCHAIN = 'combchain'
from player import Player
from table import Table
f_map = {COMB:comb,PROD:prod,CHAIN:chain}

class Combiner:
    def __init__(self) -> None:
        pass

    def _stagedCombine(self,hand,deck,n_hand,n_deck):
        if n_hand == n_deck == 0:
            return None
        if n_hand == 0:
            return FNode(f=COMB,children=[deck,n_deck]).apply()
        elif n_deck == 0:
            return FNode(f=COMB,children=[hand,n_hand]).apply()
        else:
            return FNode(f=COMBPROD,children=[[hand,n_hand],[deck,n_deck]]).apply()

    def _getPlayerCombos(self,player:Player,t:Table):
        cards_on_table = t.getCardsOnTable()[:]
        num_open = len(cards_on_table)
        bank = t.cards[:]
        x,y = player.getHand()
        if num_open == 0:
            return list(comb(bank,5))
        bank.remove(x)
        bank.remove(y)
        for c in cards_on_table:
            bank.remove(c)
        
        cots = [FNode(COMB,children=[cards_on_table,k]).apply() for k in range(num_open,num_open-3,-1)]
        max_unknowns = min(2,5 - len(cards_on_table))
        ans = []
        for i,cot in enumerate(cots):
            num_cot = num_open - i
            rest = 5 - num_cot
            for num_hand in range(2,-1,-1):
                num_unknown = max(rest - num_hand,0)
                if num_unknown <= max_unknowns and num_cot + num_hand + num_unknown == 5:
                    r = self._stagedCombine([x,y],bank,num_hand,num_unknown)
                    if not r:
                        ans.append([cards_on_table])
                    else:    
                        ans.append(FNode(f=PROD,children=[cot,r]).apply())
        return FNode(f=CHAIN,children=ans).apply()

    def _getOppCombos(self,player:Player,t:Table):
        cards_on_table = t.getCardsOnTable()[:]
        num_open =  len(cards_on_table) 
        hand = player.getHand()
        bank = t.cards[:]
        for h in hand:
            bank.remove(h)
        if num_open == 0:
            return list(comb(bank,5))
        for c in cards_on_table:
            bank.remove(c)
        cots = [FNode(COMB,children=[cards_on_table,k]).apply() for k in range(num_open,num_open-3,-1)]
        ans = []
        for i,x in enumerate(cots):
            num_cot = num_open - i
            rest = 5 - num_cot
            r = FNode(f=COMB,children=[bank,rest]).apply()
            ans.append(FNode(f=PROD,children=[x,r]).apply())
        return FNode(f=CHAIN,children=ans).apply()

class FNode:
    """
    :param: f- the function that will be applied to the children
    :param: children- list of banks/counts that will be passed to f
    :param: map- boolean: if true, maps f on children, otherwise reduces left to right
    """
    def __init__(self,f=COMB,children=[]):
        self.children = children
        self.f = f
        self.map = self.f == COMB

    def _treeApply(self):
        if self.f == COMBPROD:
            children = [FNode(f=COMB,children=x)._treeApply() for x in self.children]
            n = FNode(f=PROD,children=children)
            return n._treeApply()
        elif self.f == COMBCHAIN:
            children = [FNode(f=COMB,children=x)._treeApply() for x in self.children]
            n =  FNode(f=CHAIN,children=children)
            return n._treeApply()
        f = f_map[self.f]
        if self.map and len(self.children) == 2:
            return f(*self.children)
        if self.map:
            for i in range(len(self.children)):
                self.children[i] = f(*self.children[i])
        else:
            for i in range(len(self.children) - 1):
                self.children[i+1] = list(f(self.children[i],self.children[i+1]))

            self.children = self.children if self.map else self.children[-1]
            if self.f == PROD:
                self.children = self._combineProdIterator(self.children)
        return self.children

    def _combineProdIterator(self,l):
        res = []
        for x in l:
            r = []
            for y in x:
                r.extend(list(y))
            res.append(r)
        return res

    """
    Applies the relevant combining function to self.children
    if self.f == COMB: if self.children is [bank,num], returns choose(bank,num)
                       otherwise, maps comb on each child, which must be of the form [bank_i,num_i]
    if self.f == CHAIN: appends all the combinations in self.children together
    if self.f == PROD: equivalent to reduce(self.children,prod)
    if self.f == COMBPROD: maps comb. on each child, then reduces the result with prod
    if self.f == COMBCHAIN: maps comb. on each child, then reduces the result with chain

    """
    def apply(self):
        return list(self._treeApply())
