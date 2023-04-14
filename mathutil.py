import math

"""
Lower Incomplete Gamma Function

for Re(s) > 0:

γ(s,x) = Integral[t^(s-1)e^-t dt] from t = 0 to x

γ(s+1,x) = s * γ(s,x) - x^s * e^-t
    pf: integration by parts, not hard to convince yourself...

"""
def _LIGF(s,x,d):
    if s == 1:
        return 1 - math.exp(-x)
    return (s-1) * _LIGF(s-1,x,d/x) - d

def LIGF(s,x):
    return _LIGF(s,x,math.pow(x,s-1) * math.exp(-x))
