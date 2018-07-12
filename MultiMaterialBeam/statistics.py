import numpy as np
import blackbox
import algos
import pandas as pd
import itertools
from toolkit import *
import time
from scipy import stats
from sklearn.cluster import KMeans

def runHeuristic():
    NGEN = 5000
    verbose = False
    nVoxels = 40
    iters = 1

    fbestlist = []
    #firstlist = []
    sollist = []
    timelist = []
    freqlist = []
    poplist = []
    f1list = []
    gradlist = []
    errorLimitlist = []
    crossoverlist = []

    popArray = [40]
    f1Array = [100, 150, 200, 250, 300, 350]
    gradArray = [200, 400, 600, 800]
    timeLimitArray = [60*60]
    errorLimitArray = [0.1]
    crossoverArray = ['NotModalSixPoint']

    simu_count = len(popArray)*len(f1Array)*len(gradArray)*len(timeLimitArray)*len(errorLimitArray)*len(crossoverArray)*iters

    print("Starting simulation - estimated time: {} hours ".format(simu_count*max(timeLimitArray)/3600))
    for i, config in enumerate(list(itertools.product(popArray, f1Array, gradArray, timeLimitArray, errorLimitArray, crossoverArray))*iters):
        print("Running iteration: {}/{}, population size: {}, f1: {}, grad: {}, crossover: {}, time limit: {}s, error limit: {}%".format(i+1, simu_count, config[0], config[1], config[2], config[5], config[3], config[4]))
        benchmark = [config[1] + config[2]*x for x in range(6)]
        np.savetxt('benchmark_frequencies.txt', benchmark, fmt = '%i')

        start = time.time()
        (bin, fbest, best) = algos.GA_voxel_test(verbose, NGEN, nVoxels, config[0], timeLimit=config[3], errorLimit=config[4], crossover=config[5])
        end = time.time()
        freq = blackbox.blackbox_voxel(bin)

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
        errorLimitlist.append(config[4])
        crossoverlist.append(config[5])

    data = {'fbest': fbestlist,'sol': sollist, 'freq': freqlist, 'time': timelist, 'nPop': poplist, 'f1': f1list, 'grad': gradlist, 'errorLimit': errorLimitlist, 'crossover': crossoverlist}
    df = pd.DataFrame(data)
    df.to_csv("data.csv")

def runHeuristic_c():
    NGEN = 5000
    verbose = False
    nVoxels = 40
    iters = 40

    fbestlist = []
    #firstlist = []
    sollist = []
    timelist = []
    freqlist = []
    f1list = []
    gradlist = []
    errorLimitlist = []

    f1Array = [200]
    gradArray = [600]
    timeLimitArray = [60*60]
    errorLimitArray = [0.1]

    simu_count = len(f1Array)*len(gradArray)*len(timeLimitArray)*len(errorLimitArray)*iters

    print("Starting simulation - estimated time: {} hours ".format(simu_count*max(timeLimitArray)/3600))
    for i, config in enumerate(list(itertools.product(f1Array, gradArray, timeLimitArray, errorLimitArray))*iters):
        print("Running iteration: {}/{}, f1: {}, grad: {}, time limit: {}s, error limit: {}%".format(i+1, simu_count, config[0], config[1], config[2], config[3]))
        benchmark = [config[0] + config[1]*x for x in range(6)]
        np.savetxt('benchmark_frequencies.txt', benchmark, fmt = '%i')

        start = time.time()
        (bin, fbest, best) = algos.CMA(verbose, NGEN, nVoxels, timeLimit=config[2], errorLimit=config[3])
        end = time.time()

        E = bin[0:40]
        E = [max(10**x, 1e6) for x in E]
        rho = bin[40:80]
        rho = [max(10**(x-6), 1e1) for x in rho]
        freq = blackbox.Elmer_blackbox_continuous(E, rho)

        #sol = binaryToStr(bin)
        sol = bin
        #first = NGEN if (np.argmax(fbest<1)==0 and fbest[0]>=1) else np.argmax(fbest<1)
        timer = end - start
        frequencies = ", ".join(str(x) for x in freq)

        fbestlist.append(fbest[-1])
        # fbestlist.append(fbest)
        #firstlist.append(first)
        sollist.append(sol)
        timelist.append(timer)
        freqlist.append(frequencies)
        f1list.append(config[0])
        gradlist.append(config[1])
        errorLimitlist.append(config[3])

    data = {'fbest': fbestlist,'sol': sollist, 'freq': freqlist, 'time': timelist, 'f1': f1list, 'grad': gradlist, 'errorLimit': errorLimitlist}
    df = pd.DataFrame(data)
    df.to_csv("data.csv")

def runKMeans():
    verbose = False
    nVoxels = 40
    iters = 1

    fbestlist = []
    sollist = []
    freqlist = []
    f1list = []
    gradlist = []
    clusterlist = []

    f1Array = [200]
    gradArray = [600]
    clusterArray = ["None", 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 40]

    simu_count = len(f1Array)*len(gradArray)*len(clusterArray)*iters

    print("Starting simulation")
    for i, config in enumerate(list(itertools.product(f1Array, gradArray, clusterArray))*iters):
        print("Running iteration: {}/{}, f1: {}, grad: {}, clusters: {}".format(i+1, simu_count, config[0], config[1], config[2]))
        benchmark = [config[0] + config[1]*x for x in range(6)]
        np.savetxt('benchmark_frequencies.txt', benchmark, fmt = '%i')

        if (config[2] == "None"):

            (bin, fbest, best) = algos.CMA(verbose, 5000, nVoxels, timeLimit=60*60, errorLimit=0.1)

            E = bin[0:40]
            E = [max(10**x, 1e6) for x in E]
            rho = bin[40:80]
            rho = [max(10**(x-6), 1e1) for x in rho]
            freq = blackbox.Elmer_blackbox_continuous(E, rho)
            Ep = [np.log10(E[x]/rho[x]) for x in range(40)]

        else:

            kmeans = KMeans(n_clusters=config[2])
            s_array = np.array(Ep).reshape(-1, 1)
            kmeans.fit_predict(s_array) 
            s_labels = kmeans.labels_
            s_centers = kmeans.cluster_centers_
            avg_dis = np.sqrt(-kmeans.score(s_array)/40)

            rho_fake = [1e3]*nVoxels
            E_fake = [1e3 * 10**s_centers[s_labels[x]][0] for x in range(nVoxels)]
            bin = [np.log10(x) for x in E_fake] + [np.log10(x)+6 for x in rho_fake]
            fbest, freq = blackbox.fitness_voxel_continuous_KM(E_fake, rho_fake)
            fbest = [[fbest]]

        sol = bin
        frequencies = ", ".join(str(x) for x in freq)

        fbestlist.append(fbest[-1])
        sollist.append(sol)
        freqlist.append(frequencies)
        f1list.append(config[0])
        gradlist.append(config[1])
        clusterlist.append(config[2])

    data = {'fbest': fbestlist,'sol': sollist, 'freq': freqlist, 'f1': f1list, 'grad': gradlist, 'cluster': clusterlist}
    df = pd.DataFrame(data)
    df.to_csv("data.csv")

def main():
    runKMeans()

if __name__ == "__main__":
	main()
