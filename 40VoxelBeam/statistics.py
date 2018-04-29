import numpy as np
import blackbox
import algos
import pandas as pd
from toolkit import *
import time
import matplotlib.pyplot as plt
import seaborn as sns

def runHeuristic():
    NGEN = 100
    verbose = False
    nVoxels = 40
    iter = 50

    fbestlist = []
    firstlist = []
    sollist = []
    timelist = []
    freqlist = []

    for i in range(iter):
        print("Running iteration:", i)
        start = time.time()
        (bin, fbest, best) = algos.GA_voxel(verbose, NGEN, nVoxels)
        end = time.time()
        freq = blackbox.blackbox_voxel(bin)

        sol = binaryToStr(bin)
        first = NGEN if (np.argmax(fbest<1)==0 and fbest[0]>=1) else np.argmax(fbest<1)
        timer = end - start
        frequencies = ", ".join(str(x) for x in freq)

        fbestlist.append(fbest[-1])
        firstlist.append(first)
        sollist.append(sol)
        timelist.append(timer)
        freqlist.append(frequencies)

    data = {'fbest': fbestlist, 'first': firstlist,'sol': sollist, 'freq': freqlist, 'time': timelist}
    df = pd.DataFrame(data)
    df.to_csv("data.csv")

def makeGraphs():
    sns.set()
    data = pd.read_csv("data.csv", dtype={'time':np.float64})
    data['fbest'] = [float(x[1:-1]) for x in data['fbest']]

    ax = sns.distplot(data['time'].loc[data['fbest'] <= 1.], bins=15, kde=False, norm_hist=False, label="Reached 1% error")
    sns.distplot(data['time'].loc[data['fbest'] > 1.], bins=15, kde=False, norm_hist=False, label="Did not reach 1% error")
    ax.set(xlabel="Time taken (seconds)", ylabel="Number of occurences", title="Graph of evolution times for 50 iterations of GA")
    plt.legend()
    plt.show()

def main():
    #runHeuristic()
    makeGraphs()

if __name__ == "__main__":
	main()