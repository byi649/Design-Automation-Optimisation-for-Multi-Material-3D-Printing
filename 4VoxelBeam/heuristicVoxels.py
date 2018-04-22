import blackbox
#from Elmer_blackBox import Elmer_blackbox as blackbox
import numpy as np
import matplotlib.pyplot as plt
import algos
from toolkit import *

N = 6
#ElementOrder = 1

if __name__ == '__main__': 

    NGEN = 10
    verbose = False
    nVoxels = 4

    algorithm = "GA_voxel"

    if algorithm == "GA_voxel":
        (bin, fbest, best) = algos.GA_voxel(verbose, NGEN, nVoxels)

    print("Best solution:", bin)

    freq = blackbox.blackbox_4voxel(bin)
    print("Natural frequencies:")
    print('\n'.join('{}: {} Hz'.format(*k) for k in enumerate(freq, 1)))
	
    true_freq = [55.73843789146891, 348.21686728338096, 509.718646370548, 516.4824354644039, 974.5856546461372, 1561.7741652094128]
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