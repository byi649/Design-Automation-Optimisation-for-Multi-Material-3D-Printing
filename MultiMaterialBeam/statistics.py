import numpy as np
import blackbox
import algos
import pandas as pd
import itertools
from toolkit import *
import time
from scipy import stats

def runHeuristic():
    NGEN = 100
    verbose = False
    nVoxels = 40

    fbestlist = []
    #firstlist = []
    sollist = []
    timelist = []
    freqlist = []
    poplist = []
    f1list = []
    gradlist = []
    f1truelist = []
    gradtruelist = []

    popArray = [40]
    f1Array = [50, 100, 200, 300, 500, 800, 1000, 1500, 2000]
    gradArray = [50, 100, 200, 300, 400, 600, 800]


    for i, config in enumerate(list(itertools.product(popArray, f1Array, gradArray))):
        print("Running iteration: {}, population size: {}, f1: {}, grad: {}".format(i+1, config[0], config[1], config[2]))
        benchmark = [config[1] + config[2]*x for x in range(6)]
        np.savetxt('benchmark_frequencies.txt', benchmark, fmt = '%i')

        start = time.time()
        (bin, fbest, best) = algos.GA_voxel(verbose, NGEN, nVoxels, config[0])
        end = time.time()
        freq = blackbox.blackbox_voxel(bin)

        #slope, intercept, r_value, p_value, std_err = stats.linregress(range(1, 7), freq)
        #fbest = r_value**2

        sol = binaryToStr(bin)
        #first = NGEN if (np.argmax(fbest<1)==0 and fbest[0]>=1) else np.argmax(fbest<1)
        timer = end - start
        frequencies = ", ".join(str(x) for x in freq)

        fbestlist.append(fbest[-1])
        # fbestlist.append(fbest)
        #firstlist.append(first)
        sollist.append(sol)
        timelist.append(timer)
        freqlist.append(frequencies)
        poplist.append(config[0])
        f1list.append(config[1])
        gradlist.append(config[2])
        # f1truelist.append(slope + intercept)
        # gradtruelist.append(slope)

    #data = {'fbest': fbestlist, 'first': firstlist,'sol': sollist, 'freq': freqlist, 'time': timelist, 'nPop': poplist, 'f1': f1list, 'grad': gradlist, 'f1_true': f1truelist, 'grad_true': gradtruelist}
    data = {'fbest': fbestlist,'sol': sollist, 'freq': freqlist, 'time': timelist, 'nPop': poplist, 'f1': f1list, 'grad': gradlist}
    df = pd.DataFrame(data)
    df.to_csv("data.csv")

def main():
    runHeuristic()

if __name__ == "__main__":
	main()