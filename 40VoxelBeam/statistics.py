import numpy as np
import blackbox
import algos
import pandas as pd
from toolkit import *
import time

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

def main():
    runHeuristic()

if __name__ == "__main__":
	main()