import algos
import blackbox
from scipy import stats
import matplotlib.pyplot as plt
from toolkit import *
import pandas as pd

NGEN = 50
verbose = True
nVoxels = 40
iter = 5
nPop = 100

goal_f1 = None
goal_grad = None

def single():
    (bin, fbest, best) = algos.GA_voxel_uniform(verbose, NGEN, nVoxels, nPop, goal_f1, goal_grad)

    print("Best solution:", bin)

    freq = blackbox.blackbox_voxel(bin)
    print("Natural frequencies:")
    print('\n'.join('{}: {} Hz'.format(*k) for k in enumerate(freq, 1)))

    slope, intercept, r_value, p_value, std_err = stats.linregress(range(1,7), freq)

    print("Slope:", slope)
    print("Intercept:", intercept)
    print("r-squared:", r_value**2)

    xind = range(1,7)
    y = [intercept + x*slope for x in xind]

    plt.scatter(xind, freq)
    plt.plot(xind, y, 'r')
    plt.title("Natural frequencies from uniform-seeking objective function")
    plt.xlabel("Mode")
    plt.ylabel("Frequency (Hz)")

    plt.savefig('Uniform output')
    plt.show()

def multi():

    fbestlist = []
    sollist = []
    freqlist = []
    slopelist = []
    interceptlist = []
    rlist = []

    for i in range(iter):
        print("Running iteration:", i)
        (bin, fbest, best) = algos.GA_voxel_uniform(verbose, NGEN, nVoxels, nPop)
        freq = blackbox.blackbox_voxel(bin)
        slope, intercept, r_value, p_value, std_err = stats.linregress(range(1,7), freq)
        sol = binaryToStr(bin)
        frequencies = ", ".join(str(x) for x in freq)

        fbestlist.append(fbest[-1])
        sollist.append(sol)
        freqlist.append(frequencies)
        slopelist.append(slope)
        interceptlist.append(intercept)
        rlist.append(r_value)

    data = {'fbest': fbestlist, 'sol': sollist, 'freq': freqlist, 'slope': slopelist, 'intercept': interceptlist, 'r_value': rlist}
    df = pd.DataFrame(data)
    df.to_csv("uniform.csv")

def main():
    multi()

if __name__ == "__main__":
	main()