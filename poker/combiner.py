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
    
        

        # 2 + 46
        # 4 + 8*46
        # 6*46

        # 14*46+52 = 460 + 184 + 52 = 644 + 52 = 696

    """
    after flop:
        - use 3 cards on table
            - 2 in hand, 1 in hand 1 unknown, 2 unknowns
        - use 2 cards on table
            - 2 in hand 1 unknown, 1 in hand 2 unknown
        - use 1 card on table
            - 2 hand 2 unknown
    after turn:
        - use 4 cards on table
            - 1 in hand, 1 unknown
        - use 3 cards on table
            - 2 in hand, 1 in hand 1 unknown
        - use 2 cards on table
            - 2 in hand 1 unknown
    after river:
        - use 5 cards on table
        - use 4 cards on table
            - 1 in hand
        - use 3 cards on table
            - 2 in hand
    """
    def _getPlayerCombos(self,player:Player,t:Table):
        cards_on_table = t.getCardsOnTable()[:]
        num_unknowns = 5 - len(cards_on_table) #2 cards, and however many cards haven't been opened
        banks = t.cards[:]
        x,y = player.getHand()
        if num_unknowns == 5:
            return list(comb(banks,5))
        banks.remove(x)
        banks.remove(y)
        for c in cards_on_table:
            banks.remove(c)
        if num_unknowns == 2:
            ## x: prod []: chain, (b,c,t)k: b/c/t choose k
            # t3 x [c2,c1 x b1,b2]
            # t2 x [c2 x b1,c1 x b2]
            # t1 x (c2 x b2)
            three_c = prod(comb(cards_on_table,3), chain(chain(comb([x,y],2),prod(comb([x,y],1),comb(banks,1))),comb(banks,2)))
            two_c = prod(comb(cards_on_table,2), chain(prod(comb([x,y],2),comb(banks,1)),prod(comb([x,y],1),comb(banks,2))))
            one_c = prod(comb(cards_on_table,1), prod(comb([x,y],2),comb(banks,2)))
            ans = [three_c,two_c,one_c]
        elif num_unknowns == 1:
            # t4 x [c1,b1]
            # t3 x [c2,c1 x b1]
            # t2 x [c2 x b1]
            four_c = prod(comb(cards_on_table,4),chain(comb([x,y],1),comb(banks,1)))
            three_c = prod(comb(cards_on_table,3),chain(comb([x,y],2),prod(comb([x,y],1),comb(banks,1))))
            two_c = prod(comb(cards_on_table,2),prod(comb([x,y],2),comb(banks,1)))
            ans = [four_c,three_c,two_c]
        else:
            # t5
            # t4 x c1
            # t3 x c2
            five_c = comb(cards_on_table,5)
            four_c = prod(comb(cards_on_table,4),comb([x,y],1))
            three_c = prod(comb(cards_on_table,3),comb([x,y],2))
            ans = [five_c,four_c,three_c]
        return self._combineProdIterator(chain(chain(ans[0],ans[1]),ans[2]))

        # chain prods 
        #     each prod is between a comb and a comb or a comb and a chain or a comb and a prod
                #the chain can be longer than two, and includes combs and combprods

    def _reduce(self,f,l):
        if len(l) == 1:
            return l[0]
        for i in range(len(l)-1):
            l[i+1] = f(l[i+1],l[i])
        return l[-1]

    # def _compose(self,*fs,args=None):
    #     fs = fs[::-1]
    #     r = args
    #     for f in fs:
    #         r = self._apply(f,r)
    #     return r
        

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
    def _getOppCombos(self,player:Player,t:Table):
        cards_on_table = t.getCardsOnTable()[:]
        num_unknowns = 5 - len(cards_on_table) # the number of cards that haven't been opened
        bank = t.cards[:]
        x,y = player.getHand()
        bank.remove(x)
        bank.remove(y)
        if num_unknowns == 5:
            return list(comb(bank,5))
        for c in cards_on_table:
            bank.remove(c)
        banks = [cards_on_table,bank]
        if num_unknowns == 2:
            # cot 3 b2
            # cot 2 b3
            # cot 1 b4
            c1,c2,c3 = [3,2],[2,3],[1,4]
        elif num_unknowns == 1:
            c1,c2,c3 = [4,1],[3,2],[2,3]
            # cot 4 b1
            # cozt 3 b2
            # cot 2 b3
        else:
            c2,c3 = [4,1],[3,2]
            # cot 5
            # cot 4 b1
            # cot 3 b2
        op1 = comb(cards_on_table,5) if num_unknowns == 0 else self._getMultiCombos(banks,c1)
        op2,op3 = self._getMultiCombos(banks,c2),self._getMultiCombos(banks,c3)
        return self._combineProdIterator(chain(chain(op1,op2),op3))
    
    """
    
    :param: banks: a list of banks to select cards from 

    """
    # def _selectAndCombine(self,banks,scores,combineWith=None):
        

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
    def __init__(self,f=COMB,children=[],leaf=False,_return=True):
        self.children = children
        self.f = f
        self.map = self.f == COMB
        self.leaf = leaf
        if _return:
            return self._treeApply()
        # else self._

    def _treeApply(self):
        if self.leaf:
            return self.children[0]
        if self.f == COMBPROD:
            children = FNode(f=COMB,children=self.children)
            return FNode(f=PROD,children=children)
        elif self.f == COMBCHAIN:
            children = FNode(f=COMB,children=self.children)
            return FNode(f=CHAIN,children=self.children)
        self.f = f_map[self.f]
        if self.children:
            # if len(self.children) == 1:
            #     return self.f(self.children[0])
            if self.map:
                if len(self.children) == 1:
                    self.children[0] = self.f(*self.children)
                for i in range(len(self.children)):
                    self.children[i] = self.f(*self.children[i])
            else:
                for i in range(len(self.children) - 1):
                    self.children[i+1] = self.f(*children[i+1],*children[i])
            return self.children if self.map else self.children[-1]



def foo():
    cot = []
    hand = []
    bank = []
    lhs = FNode(f=COMB,children=[[cot,3]])
    rhs1= FNode(f=COMB,children=[hand,2])
    rhs2 = FNode(f=COMBPROD,children=[[hand,1],[bank,1]])
    rhs3 = FNode(f=COMB,children=[bank,2])
    rhs = FNode(f=CHAIN,children=[rhs1,rhs2,rhs3])
    x = FNode(f=PROD,children=[lhs,rhs])

def foo2():
    cot = []
    hand = []
    bank = []
    lhs = FNode(f=COMB,children=[cot,2])
    rhs = FNode(f=CHAIN,children=[FNode(f=COMBPROD,children=[[hand,2],[bank,1]]),FNode(f=COMBPROD,children=[[hand,1],[bank,2]])])
    x = FNode(f=PROD,children=[lhs,rhs])

def foo3():
    cot = []
    hand = []
    bank = []
    lhs = FNode(f=COMB,children=[cot,1])
    rhs = FNode(f=COMBPROD,children=[[[hand,2],[bank,1]],[hand,1],[bank,2]])
    x = FNode(f=PROD,children=[lhs,rhs])

def foo4():
    cot = []
    hand = []
    bank = []
    lhs = FNode(f=COMB,children=[cot,5])





    ## x: prod []: chain, (b,c,t)k: b/c/t choose k
    # t3 x [c2,c1 x b1,b2]
    # t2 x [c2 x b1,c1 x b2]
    # t1 x (c2 x b2)
    # cot 5
    # cot 4 b1
    # cot 3 b2