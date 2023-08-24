import unittest
from abc import abstractmethod

from allRVs import *

class TestRV:
    def __init__(self):
        self.varMap = {x:x.__name__ + 'Distribution' for x in allRVs}
        self.varMap[HyperGeometric] = 'Hypergeometric' + 'Distribution'
        self.funMap = {'pdf':'PDF',
                       'cdf':'CDF',
                       'expectedValue':'Expectation',
                       'variance':'Variance'}

    def compose(self,fun,var,args1,args2=None):
        listify = lambda x: x if type(x) == 'list' else [x]
        args1,args2 = listify(args1),listify(args2)
        base = f'{self.funMap[fun]}[{self.varMap[var]}[{",".join([str(x) for x in args1])}]'
        if args2:
            return base + ',' +  ",".join([str(x) for x in args1]) + ']'
        else:
            return base + ']'


if __name__ == '__main__':
    t = TestRV()
    for v in t.varMap:
        for f in t.funMap:
            print(t.compose(f,v,.5,.6))