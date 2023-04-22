# probably-probability             <img align='right' width="40" alt="Screenshot 2023-04-17 at 11 57 03 PM" src="https://user-images.githubusercontent.com/85849407/232667424-21c88616-f0e7-440a-b5d2-e8ccfe85fc42.png">

Work with, sample, visualize, combine, compare all your favorite random variables. 

## Supported Distributions

### Discrete

* Bernoulli
* Binomial
* Geometric
* Hyper geometric
* Poisson

### Continuous

* Uniform
* Exponential
* Normal
* Erlang

## Supported Functionalities

* Basic Functions
  * Expected value
  * PDF
  * CDF
    * Generic and recursive
  * Tail
  * Variance
  * Higher Moments [work in progress]
      * Via MGF, Laplace/z-Transform, or directly, depending on the distribution
* Simulation
  * Generate a random instance of a given distribution
    * Generic and recursive inverse transform method
    * Continuous accept/reject method
  * *k* rounds of generating independent instances of a given distribution
  * *k* independent rounds, *j* times
  * Compare sums of one distribution to other distributions
      * e.g: Erlang distribution as sum of exponentials
      * Binomials as sums of Bernoullis, etc.
* Visualization
  * Plotting
      * plot and compare any numerical function of the `RandomVariable` class with other distributions and/or other conditions of the same distribution
      * compare sampled data to the true distribution graphically
      * plot the pdf,cdf,tail etc. 

## Examples

#### Basics of Working with Distributions

* ##### Print the PDF of a Geometric Random Variable
```python
X = Geometric(0.3)
print(X.pdf(5))
> 0.072029
```

* ##### Compute the fourth moment of the Exponential distribution
    * setting `verbose` to true will print the intermediate derivatives, using the Laplace transform in the case of the Exponential distribution
```python
X = Exponential(.1)
print(X.moment(4,verbose=True)) # should be 4!/(.1^4) = 240000
> 0.1/(x + 0.1)
> -0.1/(x + 0.1)**2
> 0.2/(x + 0.1)**3
> -0.6/(x + 0.1)**4
> 240000.000000000
```

* ##### Bound the probability that a Binomial distribution deviates from its mean by at least a certain value using Chebyshev's inequality
```python
X = Binomial(100,.5)
print(u.chebyshevs(X,25)) # P[|X - E[X]| >= 25] 
> 0.04
```

* ##### Compare the PDFs of different binomial distributions 
```python

P = Plot()
P.plot({'binomial':([(20,.3),(20,.5),(20,.7)],20,1)},'pdf')
```
<img width="813" alt="Screenshot 2023-04-17 at 11 43 37 PM" src="https://user-images.githubusercontent.com/85849407/232665569-ff264196-53b9-43a5-ad0f-434ee1518e45.png">

#### Sampling

* ##### Sample a random instance of the Normal distribution
```python
X = Normal(-10,10)
print(X.genVar())
> -12.483660083014579
```

* ##### Sample some distributions for 10000 iterations
```python

util = Util()
util.simAll(k=10000)
```
<img width="813" alt="Screenshot 2023-04-17 at 10 35 53 PM" src="https://user-images.githubusercontent.com/85849407/232655813-d59862ef-ec0c-4e70-a595-a00b7af2459e.png">


* ##### Sample Poisson(10) 10000 times and compare the percentages of outcomes to the pmf graphically
```python

P = Plot()
P.plotSamples(Poisson(10),10000)
```
<img width="813" alt="Screenshot 2023-04-22 at 3 48 35 AM" src="https://user-images.githubusercontent.com/85849407/233770676-a43a1120-111f-4e3e-8f14-7672b501f287.png">

