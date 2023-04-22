from Bernoulli import Bernoulli
from Binomial import Binomial
from mathutil import avgVar
from plot import Plot
"""
Mean and Variance of Endpoint of Bounded Simple Random Walk

Let {X(t), 0 <= t <= k} be a bounded simple random walk.

N := # +1's in the process
S := End value of the process
Then: E[S] = 0 and Var(S) = k

Proof:
N = #successes in k independent Bernoulli trials with success probability 0.5
N ~ Bin(k,.5)

E[N] = E[Bin(k,.5)]
     = E[Bin(k,.5)] = k/2

S = 1 * N + (-1) * (k - N)
  = 2N - k

E[S] = 2E[N] - k = k - k = 0, as we would expect

Var(S) = E[S^2] - E[S]^2 = E[S^2]

E[S^2] = E[(2N - k)^2]
       = E[4N^2 - 4Nk + k^2]
       = 4E[N^2] - 4kE[N] + k^2
       = 4E[N^2] - k^2

E[N^2] = Var(N) + E[N]^2
       = k * .5 * (1 - .5) + (k/2)^2
       = k/4 + k^2/4

Returning to E[S^2],
4E[N^2] - k^2 = 4(k/4 + k^2/4) - k^2 = k + k^2 - k^2 = k

Thus, Var(S) = k

Alternative Calculation of Var(S):

S = X_1 + X_2 + ... + X_k

where X_i's are iid, X_i = {1 w.p .5, -1 w.p .5}
Var(X_i) = E[X_i^2] - E[X_i]^2
         = E[X_i^2] - (1/2 - 1/2)^2 = E[X_i^2]
         = (1)^2/2 + (-1)^2/2 = 1
By linearity of variance [S_n = Sum_i(X_i), X_i's iid, then Var(S_n) = Sum_i(Var(X_i))],
    Var(S) = Sum_i Var(S_i) = k


Finally, let's consider the probability S = a (for a in [-k,k])
P[S = a] = P[2N - k = a]
         = P[N = (a+k)/2] (ignoring possibly non-integral values)
         = P[Bin(k,.5) = (a+k)/2]
         = (k choose (a+k)/2)/2^k
--------------------------------------------------------------------------------------------------------------------
"""
class RandomWalk:
    def walk(self,k,j=1,verbose=True,show=False):
        X = Bernoulli(.5)
        r = []
        for _ in range(j):
            s = 0
            for _ in range(k):
                v = X.genVar()
                s += v if v else -1
            r.append(s)
        if verbose or show:
            if j == 1:
                print(f'Random Walk Endpoint for {k} iters: {s}')
            else:
                print(f'Random Walk Endpoints for {k} iters: {r}')
                avg,var = avgVar(r)
                print(f'Sample Average: {avg}; Sample Variance: {var}')
            if show:
                P = Plot()
                m = {
                    'mn':0,
                    'mx':k,
                    'f':self.walkRangeA,
                    'prefixArgs':[k],
                    'checkNone':True
                }

                chart = {
                    'xlabel': f'x: Final Value of Random Walk with {k} Steps (S)',
                    'ylabel': f'P[-x <= S <= x]',
                    'title': f'Probability of Simple Bounded {k}-step Random Walk Ending in [-x,x] ',
                }

                P.genericPlot(fInfo=m,output=True,chart=chart)

    """
    P[-a <= S_k <= a], can only be directly computed via cdf/pdf of Bin for a === k mod 1

    P[-a <= S <= a] = P[-a <= 2N - k <= a] (again for a in [-k,k])
                    = P[(k-a)/2 <= N <= (k+a)/2]
    Let c := (k-a)/2 and d := (k+a)/2
                    = P[c <= N <= d]
                    = P[N <= d] - P[N < c]      (since N is discrete, < vs. <= matters. P[N < c] = P[N <= c] - P[N = c]
                    = F_N(d) - (F_N(c) - f_N(c))
                    = F_N(d) - F_N(c) + f_N(c)
    Substituting back for c and d, we have

    P[-a <= S <= a] = F_N((k+a)/2) -  F_N((k-a)/2) + f_N(c)
    """
    def walkRangeA(self,k,a):
        if abs(a) > k:
            return
        N = Binomial(k, .5)
        c,d = (k-a)/2, (k+a)/2
        ic = int(c)
        id  = int(d)
        if ic == c and id == d:
            return N.cdf(id) - N.cdf(ic) + N.pdf(ic)
        return None

if __name__ == '__main__':
    rw = RandomWalk()
    rw.walk(30,50,show=True)