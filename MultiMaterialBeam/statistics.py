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
    iter = 12

    fbestlist = []
    firstlist = []
    sollist = []
    timelist = []
    freqlist = []
    poplist = []

    popArray = [20, 20, 20, 40, 40, 40, 60, 60, 60, 80, 80, 80]

    for i in range(iter):
        print("Running iteration:", i)
        nPop = popArray[i]
        start = time.time()
        (bin, fbest, best) = algos.GA_voxel(verbose, NGEN, nVoxels, nPop)
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
        poplist.append(nPop)

    data = {'fbest': fbestlist, 'first': firstlist,'sol': sollist, 'freq': freqlist, 'time': timelist, 'nPop': poplist}
    df = pd.DataFrame(data)
    df.to_csv("data.csv")

def main():
    runHeuristic()

if __name__ == "__main__":
	main()