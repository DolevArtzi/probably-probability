from allRVs import *

"""
You have 3 GoPro batteries for the ski day.
The time that battery i lasts is independently 
distributed as exponentially distributed with an expected lifetime
of 3hr. What is the probability that your batteries last 
for 7 hours of skiing? How about 8.5?

BatteryLife_i ~ Exponential(1/3)
X ~ Erlang(3,1/3)
P[X > k hrs] = ?
"""
def p1():
    return Erlang(3,1/3).tail(7),Erlang(3,1/3).tail(8.5)

if __name__ == '__main__':
    print(p1())