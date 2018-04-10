import algos
from toolkit import *
import numpy as np
import matplotlib.pyplot as plt

global NGEN
NGEN = 250

def algorithm_wrapper(algorithm):
    verbose = False
    if algorithm == "GA":
        (E, fbest, best) = algos.GA(verbose, NGEN)
        (E, rho) = binaryToVar(E)
    elif algorithm == "CMA":
        (E, rho, fbest, best) = algos.CMA(verbose, NGEN)
    elif algorithm == "GA_1":
        (E, fbest, best) = algos.GA_1(verbose, NGEN)
        (E, rho) = binaryToVar(E)

    fbest = [x[0] for x in fbest]
    return fbest

GA_runs = []
CMA_runs = []
GA_1_runs = []

niter = 50
for i in range(niter):
    GA_runs.append(algorithm_wrapper("GA"))
    CMA_runs.append(algorithm_wrapper("CMA"))
    GA_1_runs.append(algorithm_wrapper("GA_1"))

GA_runs = np.vstack(GA_runs)
CMA_runs = np.vstack(CMA_runs)
GA_1_runs = np.vstack(GA_1_runs)

GA_first = [0,0,0]
CMA_first = [0,0,0]
GA_1_first = [0,0,0]

for i in range(niter):
    GA_first[0] += np.argmax(GA_runs[i]<1)
    CMA_first[0] += np.argmax(CMA_runs[i]<1)
    GA_1_first[0] += np.argmax(GA_1_runs[i]<1)
    GA_first[1] += np.argmax(GA_runs[i]<0.1)
    CMA_first[1] += np.argmax(CMA_runs[i]<0.1)
    GA_1_first[1] += np.argmax(GA_1_runs[i]<0.1)
    GA_first[2] += np.argmax(GA_runs[i]<0.01)
    CMA_first[2] += np.argmax(CMA_runs[i]<0.01)
    GA_1_first[2] += np.argmax(GA_1_runs[i]<0.01)

GA_first[0] = GA_first[0] / niter
CMA_first[0] = CMA_first[0] / niter
GA_1_first[0] = GA_1_first[0] / niter
GA_first[1] = GA_first[1] / niter
CMA_first[1] = CMA_first[1] / niter
GA_1_first[1] = GA_1_first[1] / niter
GA_first[2] = GA_first[2] / niter
CMA_first[2] = CMA_first[2] / niter
GA_1_first[2] = GA_1_first[2] / niter


x = list(range(NGEN))
for i in range(niter):
    plt.subplot(2, 2, 1)
    plt.semilogy(x, GA_runs[i])
    plt.title("Objective function (GA)")
    plt.subplot(2, 2, 2)
    plt.semilogy(x, CMA_runs[i])
    plt.title("Objective function (CMA)")
    plt.subplot(2, 2, 3)
    plt.semilogy(x, GA_1_runs[i])
    plt.title("Objective function (GA_1)")

    ax = plt.subplot(2, 2, 4)

    N = 3
    ind = np.arange(N)  # the x locations for the groups
    width = 0.27       # the width of the bars

    rects1 = ax.bar(ind, [GA_first[0], CMA_first[0], GA_1_first[0]], width, color='r')
    rects2 = ax.bar(ind+width, [GA_first[1], CMA_first[1], GA_1_first[1]], width, color='g')
    rects3 = ax.bar(ind+width*2, [GA_first[2], CMA_first[2], GA_1_first[2]], width, color='b')

    ax.set_ylabel('Generation number')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ('GA', 'CMA', 'GA_1') )
    ax.legend( (rects1[0], rects2[0], rects3[0]), ('1%', '0.1%', '0.01%') )

    plt.title("Generations to reach accuracy")
plt.show()