import blackbox
import numpy as np
import matplotlib.pyplot as plt
import algos
from toolkit import *

N = 6
#ElementOrder = 1

if __name__ == '__main__': 

    NGEN = 10
    verbose = True
    nVoxels = 40

    algorithm = "GA_voxel"

    if algorithm == "GA_voxel":
        (bin, fbest, best) = algos.GA_voxel(verbose, NGEN, nVoxels)

    print("Best solution:", bin)

    freq = blackbox.blackbox_voxel(bin)
    print("Natural frequencies:")
    print('\n'.join('{}: {} Hz'.format(*k) for k in enumerate(freq, 1)))
	
    true_freq = np.loadtxt('benchmark_frequencies.txt')
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

    # plt.subplot(2, 2, 3)
    # plt.plot(x, best)
    # plt.grid(True)
    # plt.title("Blue: E, orange: rho (*1e6)")

    plt.subplot(2, 2, 4)
    plt.bar(x=range(1, N + 1), height=errors)
    print(errors)
    plt.title("Percentage error for each mode")

    ax = plt.gca()
    ax.set_ylim(bottom=min(errors)-np.std(errors), top=max(errors)+np.std(errors))

    plt.show()
