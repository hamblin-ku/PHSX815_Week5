# PHSX815_Week5

## Homework 5: Rejection Sampling
`rejection_fig.png` contains the results from rejection sampling from a target dsitribution (that happens to be the sum of three different normal distributions). I sampled with a wide normal distribution that I scaled to encompass the entrie target curve. With 10,000 iterations, I achieved an efficiency of 48.9%.

## Homework 6: Numerical Integration
I implemetned trapezoidal integration and gaussian quadrature integration functions in my `integration.py`. For my test function, I chose
```
f(x) = 1 / (1 + x^2)
```
the analytic solution for this is known to be arctan(x), so comparison to the "true" solution is easy. I evalauted on the closed interval [0,10] using different numbers of sub-intervals. I found that the integrations quickly convered (likely due to the overall simple shape of the function), so in `Homework6.png` I chose to only show sub-intervals up to 30.

It is readily apparent that the gaussian quadrature integration converges much quicker to the analytic solution, needing only about ~10 sub-intervals to converge well.

## Usage
The scripts can be ran as:

-`python python/rejection_sampling.py --Niter [# iterations]` 
-`python python/intergration.py -n [# of sub intervals to plot]`
