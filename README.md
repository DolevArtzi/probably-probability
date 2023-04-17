# probably-probability
Work with all your favorite random variables.

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
  * Higher Moments
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

  
