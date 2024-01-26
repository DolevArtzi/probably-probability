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
                    print(num_open,num_cot,num_hand,num_unknown)
                    # l = FNode(f=COMB,children=[x,num_cot]).apply()
                    r = self._stagedCombine([x,y],bank,num_hand,num_unknown)
                    # r = self._combineProdIterator(r)
                    if not r:
                        ans.append([cards_on_table])
                    else:    
                        ans.append(FNode(f=PROD,children=[cot,r]).apply())
                    # print('l',x)
                    # print('r',r)
                    # print(type(ans),'ans',ans,num_cot,num_hand,num_unknown)
        return FNode(f=CHAIN,children=ans).apply()

# hey there
# 3 3 2 0
# l []
# r [([(33, 6, 40)], 20)]
# <class 'list'> ans [[]] 3 2 0


    """"
    after the flop:

    opp can use either all three on the table and two unknowns c2
    or two from the table and three unknowns c3*3c1
    or one from the table and four unknowns 3c1*c4

    after the turn:

    opp can use all four and one mystery 
    opp can use three and two mysteries 
    opp can use two and three mysteries 

    after the river:
    opp can use five
    opp can use four and one mystery
    opp can use three and two mysteries 
    """

    '''
    lists all of the possible combinations your opponents can have, depending on the stage of the hand
    returns: iterator of 1-52 hands
    '''
    # def _getOppCombos(self,player:Player,t:Table):
    #     cards_on_table = t.getCardsOnTable()[:]
    #     num_unknowns = 5 - len(cards_on_table) # the number of cards that haven't been opened
    #     bank = t.cards[:]
    #     x,y = player.getHand()
    #     bank.remove(x)
    #     bank.remove(y)
    #     if num_unknowns == 5:
    #         return list(comb(bank,5))
    #     for c in cards_on_table:
    #         bank.remove(c)
    #     banks = [cards_on_table,bank]
    #     if num_unknowns == 2:
    #         # cot 3 b2
    #         # cot 2 b3
    #         # cot 1 b4
    #         c1,c2,c3 = [3,2],[2,3],[1,4]
    #     elif num_unknowns == 1:
    #         c1,c2,c3 = [4,1],[3,2],[2,3]
    #         # cot 4 b1
    #         # cozt 3 b2
    #         # cot 2 b3
    #     else:
    #         c2,c3 = [4,1],[3,2]
    #         # cot 5
    #         # cot 4 b1
    #         # cot 3 b2
    #     op1 = comb(cards_on_table,5) if num_unknowns == 0 else self._getMultiCombos(banks,c1)
    #     op2,op3 = self._getMultiCombos(banks,c2),self._getMultiCombos(banks,c3)
    #     return self._combineProdIterator(chain(chain(op1,op2),op3))
    

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
            # ans.append(FNode(f=COMBPROD,children=[[x,num_cot],[bank,rest]]).apply())
            # for num_hand in range(2,-1,-1):
            #     # num_unknown = rest - num_hand
            #     l = FNode(f=COMBPROD,children=[[x,num_cot],[bank,rest]]).apply()
            #     ans.append(l)
                # ans.append(self._stagedCombine(cots,[],bank,num_cot,0,num_unknown))
        return FNode(f=CHAIN,children=ans).apply()




            # return 0
            ## x: prod []: chain, (b,c,t)k: b/c/t choose k
            # t3 x [c2,c1 x b1,b2]
            # t2 x [c2 x b1,c1 x b2]
            # t1 x (c2 x b2)

            

        #     three_c = prod(comb(cards_on_table,3), chain(chain(comb([x,y],2),prod(comb([x,y],1),comb(banks,1))),comb(banks,2)))
        #     two_c = prod(comb(cards_on_table,2), chain(prod(comb([x,y],2),comb(banks,1)),prod(comb([x,y],1),comb(banks,2))))
        #     one_c = prod(comb(cards_on_table,1), prod(comb([x,y],2),comb(banks,2)))
        #     ans = [three_c,two_c,one_c]
        # elif num_open == 4:
        #     # t4 x [c1,b1]
        #     # t3 x [c2,c1 x b1]
        #     # t2 x [c2 x b1]
        #     four_c = prod(comb(cards_on_table,4),chain(comb([x,y],1),comb(banks,1)))
        #     three_c = prod(comb(cards_on_table,3),chain(comb([x,y],2),prod(comb([x,y],1),comb(banks,1))))
        #     two_c = prod(comb(cards_on_table,2),prod(comb([x,y],2),comb(banks,1)))
        #     ans = [four_c,three_c,two_c]
        # else:
        #     # t5
        #     # t4 x c1
        #     # t3 x c2
        #     five_c = comb(cards_on_table,5)
        #     four_c = prod(comb(cards_on_table,4),comb([x,y],1))
        #     three_c = prod(comb(cards_on_table,3),comb([x,y],2))
        #     ans = [five_c,four_c,three_c]
        # return self._combineProdIterator(chain(chain(ans[0],ans[1]),ans[2]))
        
    def _reduce(self,f,l):
        if len(l) == 1:
            return l[0]
        for i in range(len(l)-1):
            l[i+1] = f(l[i+1],l[i])
        return l[-1]

    #support product, chaining, combinations, name is short for multichoose
    def _mc(self,counts=None,op=PROD,*banks):
        if op == COMBPROD: #reduce(prod,map(comb,banks))
            # if counts is shorter than banks, will exclude the first entry of banks from the comb.
            if len(counts) < len(banks):
                cards_on_table = banks[0]
                banks = banks[1:]
            combs = [self._mc([counts[i+1]],b,op=COMB) for i,b in enumerate(banks)]
            return self._reduce(prod,combs)
        if op == PROD:
            return prod(banks[0],banks[1])
        if op == COMB:
            l = [comb(b,counts[i]) for i,b in enumerate(banks)]
        else:
            l = banks
        return self._reduce(chain,l)




    

    """
    Generate the combinations, either for 'you' or your opponent, given the cards on the table,
    the remaining cards in the deck, and possibly a hand, if for 'you'

    :param: cards_on_table: list of the cards that have been opened on the table
    :param: bank: the remaining cards in the deck, besides the open cards and possibly 'your' hand
    :param: counts:
                # - if hand == None: 
                #     [number to choose from table, number to choose from bank]
                # - if hand == (x,y):
                #     [number to choose from table, ]

    """
    def _generateCombos(self,cards_on_table,bank,counts,hand=None):
        if hand:
            for c in hand: bank.remove(c)
        num_open = len(cards_on_table)
        mc = self._mc
        if num_open == 0:
            return comb(bank,5)
        if num_open == 3:
            if hand:
                r1 = mc(mc([2],hand,op=COMB),mc([1,1],hand,bank,op=COMB),mc([2],bank,op=COMB), op=CHAIN,counts=None)
                x1 = mc(None,mc([3],cards_on_table,op=COMB),r1,op=PROD)
                r2 = mc(mc([2],hand,op=COMB),mc([1,1],hand,bank,op=COMB),mc([2],bank,op=COMB), op=CHAIN,counts=None)
                x2 = mc(None,mc([2],cards_on_table,op=COMB),r2,op=PROD)
            ## x: prod []: chain, (b,c,t)k: b/c/t choose k
            # t3 x [c2,c1 x b1,b2]
            # t2 x [c2 x b1,c1 x b2]
            # t1 x (c2 x b2)

        #solo choose
        #tk x [ck,b/c k x b/c k, ...]  {also '( .. )' for solo}


    def _combineProdIterator(self,*iter,l=False):
        if l:
            return list(chain(*iter))
        else:
            l_iter = list(iter)
            print(l_iter[:20],'in combine prod iter. false')

#         x = [(1,2,3),(4,5,6),(7,)]
# def z(*a):
#     for aa in a:
#         print(aa)
            l_iter = [self._combineProdIterator(h,True) for h in l_iter]
            return l_iter


    """
    
    :param: banks: a list of banks to select cards from 

    """

    def _getCombos2(self,cards_on_table,bank,n1,n2):
        return prod(comb(cards_on_table,n1),comb(bank,n2))

    def _getMultiCombos(self,banks,counts):
        partial = [comb(banks[i],counts[i]) for i in range(len(banks))]
        for i in range(len(banks) - 1):
            partial[i+1] = prod(partial[i+1],partial[i])
        return partial[-1]

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

    def _foo(self,*args):
        for x in args:
            print('x',x)

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
                # if self.f == PROD:
                #     print('aaaaaaaa',self.children[i+1])
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


    def apply(self):
        return list(self._treeApply())


# def foo():
#     cot = []
#     hand = []
#     bank = []
#     lhs = FNode(f=COMB,children=[[cot,3]])
#     rhs1= FNode(f=COMB,children=[hand,2])
#     rhs2 = FNode(f=COMBPROD,children=[[hand,1],[bank,1]])
#     rhs3 = FNode(f=COMB,children=[bank,2])
#     rhs = FNode(f=CHAIN,children=[rhs1,rhs2,rhs3])
#     x = FNode(f=PROD,children=[lhs,rhs])

# def foo2():
#     cot = []
#     hand = []
#     bank = []
#     lhs = FNode(f=COMB,children=[cot,2])
#     rhs = FNode(f=CHAIN,children=[FNode(f=COMBPROD,children=[[hand,2],[bank,1]]),FNode(f=COMBPROD,children=[[hand,1],[bank,2]])])
#     x = FNode(f=PROD,children=[lhs,rhs])

# def foo3():
#     cot = []
#     hand = []
#     bank = []
#     lhs = FNode(f=COMB,children=[cot,1])
#     rhs = FNode(f=COMBPROD,children=[[[hand,2],[bank,1]],[hand,1],[bank,2]])
#     x = FNode(f=PROD,children=[lhs,rhs])

# def foo4():
#     cot = []
#     hand = []
#     bank = []
#     lhs = FNode(f=COMB,children=[[cot,5]])





    ## x: prod []: chain, (b,c,t)k: b/c/t choose k
    # t3 x [c2,c1 x b1,b2]
    # t2 x [c2 x b1,c1 x b2]
    # t1 x (c2 x b2)
    # cot 5
    # cot 4 b1
    # cot 3 b2