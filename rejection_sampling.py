# File:     rejection_sampling.py
# Author:   Kurt Hamblin
# Description:  Analyze outputs from the monopoly simulation in monopoly_experiment.py

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse
from Random import Random
import matplotlib
import seaborn as sns

# Import my custom matplotlib config and activate it
import my_params
custom_params = my_params.params()
matplotlib.rcParams.update(custom_params)

# Probability Density function for normal distribution
def normal_dist(x , mean , sd):
    return 1/np.sqrt(2*np.pi*sd**2) * np.exp(-0.5*((x-mean)/sd)**2)

# Target distribution
def target_func(x):
    return (normal_dist(x, 20, 10) + normal_dist(x, 70, 30) + normal_dist(x, 50, 10))/3

# Proposal distribution
def prop_func(x):
    return normal_dist( x, 50, 40)



# main function for this Python code
if __name__ == "__main__":

    # Set up parser to handle command line arguments
    # Run as 'python monopoly_analysis.py -h' to see all available commands
    parser = argparse.ArgumentParser()
    parser.add_argument("--Niter",  help="Number of iterations")
    args = parser.parse_args()
    
    Niter = 1000
    if args.Niter:
        Niter = int(args.Niter)

    x_plot = np.linspace(-100, 300, 1000)
    
    # We must scale the proposal distribution so that it contains the target
    C = 1.2*np.max(target_func(x_plot)) / np.max(prop_func(x_plot))
    # If proposal dist already encompasses the target, no need to scale
    if C < 1:
        C = 1
    
    
    # Perform Rejection Samping
    sample = np.array([])
    rand = Random()
    num_accepted = 0
    for i in range(Niter):
        # Draw random num from proposal dsitribution
        rand_X = np.random.normal( 50, 40)
        # Draw (unformly) y value
        rand_Y = rand.rand()*C*prop_func(rand_X)
        
        # If the drawn Y value is under the target curve, accept rand_X
        if rand_Y <= target_func(rand_X):
            num_accepted += 1
            sample = np.append(sample, rand_X)

    logN = int(np.log10(Niter))
    eff = num_accepted/Niter*100
    print(f'Number Accepted: {num_accepted}')
    print(f'Efficiency: {eff:.4f}%')
    
    fig, ax = plt.subplots()
    ax.set_xlim([-100,200])
    ax.set_ylim([0,0.03])
    ax.set_ylabel('Probability')
    ax.set_xlabel('x')
    ax.plot(x_plot, target_func(x_plot), c = 'r', lw = 3, label = 'Target')
    ax.plot(x_plot, prop_func(x_plot), c = 'k', lw = 2, linestyle = '--', label = 'Proposed')
    ax.plot(x_plot, C*prop_func(x_plot), c = 'g', lw = 2, linestyle = '--', label = 'Scaled Proposed')
    ax.hist(sample, bins = 50 , density = True, alpha = 0.4, label = 'Sample dist.')
    ax.annotate(f'log(N) = {logN}', (-80, 0.027))
    ax.annotate(f'Efficiency = {eff:.1f}\%', (-80, 0.025))
    ax.legend(loc='upper right')
    
    plt.show()
