import blackbox
import numpy as np
import matplotlib.pyplot as plt
import algos
from toolkit import *

N = 6

if __name__ == '__main__': 

    NGEN = 250
    verbose = False

    algorithm = "PSO"

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

    print("Best solution: E = {0:.3e}, rho = {1:.3e}".format(E, rho*1e-6))

    freq = blackbox.blackbox(E, rho*1e-6)
    print("Natural frequencies:")
    print('\n'.join('{}: {} Hz'.format(*k) for k in enumerate(freq, 1)))

    true_freq = [53.005922156059206, 332.20641980613505, 930.2811671037335, 1822.8783393540868, 3013.3294997485928, 4501.393450241724, 6287.070190833485, 8370.359721523866, 10751.262042312881, 13429.777153200515]
    true_freq = true_freq[:N]


    errors = []
    for i in range(N):
        errors.append(abs(freq[i] - true_freq[i]) / true_freq[i] * 100)
    errors = np.array(errors)

    print("Average error: {0:.3e}%".format(np.average(errors)))

    # X-axis = generation
    x = list(range(NGEN))
    plt.figure()
    plt.subplot(2, 2, 2)
    plt.semilogy(x, fbest, "-c")
    plt.grid(True)
    plt.title("Average percentage error (log)")

    plt.subplot(2, 2, 1)
    plt.plot(x, fbest, "-c")
    plt.grid(True)
    plt.title("Average percentage error")

    plt.subplot(2, 2, 3)
    plt.plot(x, best)
    plt.grid(True)
    plt.title("Blue: E, orange: rho (*1e6)")

    plt.subplot(2, 2, 4)
    plt.bar(x=range(1, N + 1), height=errors)
    print(errors)
    plt.title("Percentage error for each mode")

    ax = plt.gca()
    ax.set_ylim(bottom=min(errors)-np.std(errors), top=max(errors)+np.std(errors))

    plt.show()