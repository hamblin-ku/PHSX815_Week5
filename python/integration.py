# File:     rejection_sampling.py
# Author:   Kurt Hamblin
# Description:  Use rejection sampling to sample a target distribution

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse
import matplotlib
from scipy.special.orthogonal import p_roots

# Import my custom matplotlib config and activate it
import my_params
custom_params = my_params.params()
matplotlib.rcParams.update(custom_params)



def int_trap(f, a, b, N = 100):
    # correct in case user entered interval bounds backwards
    if b < a:
        a, b  = b, a
    # interval width
    dx = (b-a)/N
    
    # First add the edges
    total = 0.5*f(a) + 0.5*f(b)
    for i in range(1,N):
        total += f(a + i*dx)
    return dx*total

def int_quad(f, a, b, n):
    x, weights = p_roots(n+1)
    gauss = 0.5*(b-a)*np.sum(weights*f( 0.5*(b - a)*x + 0.5*(b + a) ) )
    return gauss

# main function for this Python code
if __name__ == "__main__":

    # Set up parser to handle command line arguments
    # Run as 'python monopoly_analysis.py -h' to see all available commands
    parser = argparse.ArgumentParser()
    parser.add_argument("-n","--Nsub",  help="Number of sub-interval bins to evaluate")
    args = parser.parse_args()
    
    N = 100
    if args.Nsub:
        N = int(args.Nsub)

    # We will integrate the following. Analytic solution is arctan(x)
    f_test= lambda x: 1/(1 + x**2)
    
    # sub intervals to evaluate for
    N_sub_intervals = np.linspace(2, 30, N, dtype= int)
    
    # store evaluated integrals
    trap = np.zeros(N)
    quad = np.zeros(N)
    
    # We will integrate from 0 to 10
    for i, Nsub in enumerate(N_sub_intervals):
        trap[i] = int_trap(f_test, 0, 10, Nsub)
        quad[i] = int_quad(f_test,0, 10, Nsub)
    
    # Evaluate errors compared to analytic solution
    true_integral = np.arctan(10)
    err_trap = np.array( [val - true_integral for val in trap])
    err_quad = np.array( [val - true_integral for val in quad])
    
    
    
    fig, ax = plt.subplots(2, 1, figsize = (7, 9), sharex = True, gridspec_kw = {'height_ratios':[2,1]})
    fig.subplots_adjust(hspace = 0.001)
    ax[1].set_ylim([-0.003, 0.01])
    ax[0].set_ylim([1.35,2.5])
    ax[0].plot(N_sub_intervals, trap, c = 'green', label = 'trapz')
    ax[0].plot(N_sub_intervals, quad, c = 'slateblue', label = 'gauss quad')
    ax[0].plot(N_sub_intervals, [true_integral]*N,  label = 'analytic sol.', c= 'k', lw = 3, ls='dotted')
    
    ax[1].plot(N_sub_intervals, [0]*N,  label = 'analytic sol.', c= 'k', lw = 3, ls='dotted')
    ax[1].plot(N_sub_intervals, err_trap, c = 'green', label = 'trapz', zorder = 0)
    ax[1].plot(N_sub_intervals, err_quad, c = 'slateblue', label = 'gauss quad', zorder = 0)
    
    ax[0].set_xlim([1,30])
    ax[0].legend(loc = 'upper right', fontsize = 18)
    ax[0].set_ylabel('Integral Value', fontsize = 20)
    ax[1].set_xlabel('N samples', fontsize = 20)
    ax[1].set_ylabel('Error', fontsize = 20)
    plt.show()
