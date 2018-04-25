import blackbox
import numpy as np
import matplotlib.pyplot as plt
import algos
from toolkit import *

N = 6
#ElementOrder = 1

if __name__ == '__main__': 

    NGEN = 250
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

    gs = plt.GridSpec(4, 4)

    # X-axis = generation
    x = list(range(NGEN))
    plt.figure()
    plt.subplot(gs[0:2,2:4])
    plt.semilogy(x, fbest, "-c")
    plt.grid(True)
    plt.title("Average percentage error (log)")
    ax = plt.gca()
    ax.set_ylabel('Error(%)')
    ax.set_xlabel('Generation number')

    plt.subplot(gs[0:2,0:2])
    plt.plot(x, fbest, "-c")
    plt.grid(True)
    plt.title("Average percentage error")
    ax = plt.gca()
    ax.set_ylabel('Error(%)')
    ax.set_xlabel('Generation number')

    plt.subplot(gs[2,0:2])
    plt.imshow([bin])
    plt.title("Beam voxels: yellow = AL, blue = PLA")
    plt.axis("off")

    goal = np.loadtxt('material_array.txt')
    plt.subplot(gs[3,0:2])
    plt.imshow([goal])
    plt.title("True voxels: yellow = AL, blue = PLA")
    plt.axis("off")

    plt.subplot(gs[2:4,2:4])
    plt.bar(x=range(1, N + 1), height=errors)
    print(errors)
    plt.title("Percentage error for each mode")

    ax = plt.gca()
    ax.set_ylim(bottom=min(errors)-np.std(errors), top=max(errors)+np.std(errors))

    plt.tight_layout()
    plt.savefig('Heuristic output')
    plt.show()
