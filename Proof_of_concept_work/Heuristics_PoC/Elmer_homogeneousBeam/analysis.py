import algos
from toolkit import *
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__': 
    global NGEN
    NGEN = 10

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
        elif algorithm == "PSO":
            (E, rho, fbest, best) = algos.PSO(verbose, NGEN)

        fbest = [x[0] for x in fbest]
        return fbest

    GA_runs = []
    CMA_runs = []
    GA_1_runs = []
    PSO_runs = []

    niter = 10
    for i in range(niter):
        print("Evaluating iteration:", i)
        GA_runs.append(algorithm_wrapper("GA"))
        CMA_runs.append(algorithm_wrapper("CMA"))
        GA_1_runs.append(algorithm_wrapper("GA_1"))
        PSO_runs.append(algorithm_wrapper("PSO"))

    GA_runs = np.vstack(GA_runs)
    CMA_runs = np.vstack(CMA_runs)
    GA_1_runs = np.vstack(GA_1_runs)
    PSO_runs = np.vstack(PSO_runs)

    GA_first = [0,0,0]
    CMA_first = [0,0,0]
    GA_1_first = [0,0,0]
    PSO_first = [0,0,0]

    for i in range(niter):
        GA_first[0] += np.argmax(GA_runs[i]<1)
        CMA_first[0] += np.argmax(CMA_runs[i]<1)
        GA_1_first[0] += np.argmax(GA_1_runs[i]<1)
        PSO_first[0] += np.argmax(PSO_runs[i]<1)

        GA_first[1] += np.argmax(GA_runs[i]<0.1) if np.argmax(GA_runs[i]<0.1) > 0 else NGEN
        CMA_first[1] += np.argmax(CMA_runs[i]<0.1) if np.argmax(CMA_runs[i]<0.1) > 0 else NGEN
        GA_1_first[1] += np.argmax(GA_1_runs[i]<0.1) if np.argmax(GA_1_runs[i]<0.1) > 0 else NGEN
        PSO_first[1] += np.argmax(PSO_runs[i]<0.1) if np.argmax(PSO_runs[i]<0.1) > 0 else NGEN

        GA_first[2] += np.argmax(GA_runs[i]<0.01) if np.argmax(GA_runs[i]<0.01) > 0 else NGEN
        CMA_first[2] += np.argmax(CMA_runs[i]<0.01) if np.argmax(CMA_runs[i]<0.01) > 0 else NGEN
        GA_1_first[2] += np.argmax(GA_1_runs[i]<0.01) if np.argmax(GA_1_runs[i]<0.01) > 0 else NGEN
        PSO_first[2] += np.argmax(PSO_runs[i]<0.01) if np.argmax(PSO_runs[i]<0.01) > 0 else NGEN

    GA_first[0] = GA_first[0] / niter
    CMA_first[0] = CMA_first[0] / niter
    GA_1_first[0] = GA_1_first[0] / niter
    PSO_first[0] = PSO_first[0] / niter

    GA_first[1] = GA_first[1] / niter
    CMA_first[1] = CMA_first[1] / niter
    GA_1_first[1] = GA_1_first[1] / niter
    PSO_first[1] = PSO_first[1] / niter

    GA_first[2] = GA_first[2] / niter
    CMA_first[2] = CMA_first[2] / niter
    GA_1_first[2] = GA_1_first[2] / niter
    PSO_first[2] = PSO_first[2] / niter


    x = list(range(NGEN))
    for i in range(niter):
        plt.subplot(3, 2, 1)
        plt.semilogy(x, GA_runs[i])
        plt.title("Objective function (GA)")

        ax = plt.gca()
        ax.set_ylim(bottom = 1e-13, top = 1e2)

        plt.subplot(3, 2, 2)
        plt.semilogy(x, CMA_runs[i])
        plt.title("Objective function (CMA)")

        ax = plt.gca()
        ax.set_ylim(bottom = 1e-13, top = 1e2)

        plt.subplot(3, 2, 3)
        plt.semilogy(x, GA_1_runs[i])
        plt.title("Objective function (GA_1)")

        ax = plt.gca()
        ax.set_ylim(bottom = 1e-13, top = 1e2)

        plt.subplot(3, 2, 4)
        plt.semilogy(x, PSO_runs[i])
        plt.title("Objective function (PSO)")

        ax = plt.gca()
        ax.set_ylim(bottom = 1e-13, top = 1e2)

        ax = plt.subplot(3, 1, 3)

        N = 4
        ind = np.arange(N)  # the x locations for the groups
        width = 0.27       # the width of the bars

        rects1 = ax.bar(ind, [GA_first[0], CMA_first[0], GA_1_first[0], PSO_first[0]], width, color='r')
        rects2 = ax.bar(ind+width, [GA_first[1], CMA_first[1], GA_1_first[1], PSO_first[1]], width, color='g')
        rects3 = ax.bar(ind+width*2, [GA_first[2], CMA_first[2], GA_1_first[2], PSO_first[2]], width, color='b')

        ax.set_ylabel('Generation number')
        ax.set_xticks(ind+width)
        ax.set_xticklabels( ('GA', 'CMA', 'GA_1', 'PSO') )
        ax.legend( (rects1[0], rects2[0], rects3[0]), ('1%', '0.1%', '0.01%') )

        plt.title("Generations to reach accuracy")
    plt.show()