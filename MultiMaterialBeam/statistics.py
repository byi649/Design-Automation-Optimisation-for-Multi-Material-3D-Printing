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
    iters = 5

    fbestlist = []
    fhistorylist = []
    fhistorylistbk = []
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
    f1Array = [25, 50, 75]
    gradArray = [100, 150, 200, 250]
    timeLimitArray = [60*60]
    errorLimitArray = [0.01]
    crossoverArray = ['ModalSixPoint']

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
        fhistorylist.append(fbest)
        fhistorylistbk.append(list(fbest))
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

    data = {'fbest': fbestlist,'sol': sollist, 'freq': freqlist, 'time': timelist, 'nPop': poplist, 'f1': f1list, 'grad': gradlist, 'errorLimit': errorLimitlist, 'crossover': crossoverlist, 'fhistory': fhistorylist, 'fhistorybk': fhistorylistbk}
    df = pd.DataFrame(data)
    df.to_csv("data.csv")

def runHeuristic_c():
    NGEN = 5000
    verbose = False
    nVoxels = 40
    iters = 1

    fbestlist = []
    sollist = []
    timelist = []
    freqlist = []
    f1list = []
    gradlist = []
    errorLimitlist = []
    clusterslist = []

    f1Array = [200]
    gradArray = [600]
    timeLimitArray = [60*20]
    errorLimitArray = [0.1]
    clustersArray = [0, 5, 10, 20]

    simu_count = len(f1Array)*len(gradArray)*len(timeLimitArray)*len(errorLimitArray)*len(clustersArray)*iters

    print("Starting simulation - estimated time: {} hours ".format(simu_count*max(timeLimitArray)/3600))
    for i, config in enumerate(list(itertools.product(f1Array, gradArray, timeLimitArray, errorLimitArray, clustersArray))*iters):
        print("Running iteration: {}/{}, f1: {}, grad: {}, time limit: {}s, error limit: {}%, clusters: {}%".format(i+1, simu_count, config[0], config[1], config[2], config[3], config[4]))
        benchmark = [config[0] + config[1]*x for x in range(6)]
        np.savetxt('benchmark_frequencies.txt', benchmark, fmt = '%i')

        start = time.time()
        (bin, fbest, best) = algos.CMA_ratio(verbose, NGEN, nVoxels, timeLimit=config[2], errorLimit=config[3], clusters=config[4])
        end = time.time()

        if config[4] == 0:
            E = [10**(3*x) for x in bin]
            rho = [1e3]*40
            freq = blackbox.Elmer_blackbox_continuous(E, rho)
        else:
            (fbest, freq, bin) = blackbox.fitness_voxel_continuous_ratio_KM(bin, config[4])
            fbest = [[fbest]]

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
        clusterslist.append(config[4])

    data = {'fbest': fbestlist,'sol': sollist, 'freq': freqlist, 'time': timelist, 'f1': f1list, 'grad': gradlist, 'errorLimit': errorLimitlist, 'clusters': clusterslist}
    df = pd.DataFrame(data)
    df.to_csv("data.csv")

def runKMeans():
    verbose = False
    nVoxels = 40
    iters = 10
    timeLimit = 60*60

    fbestlist = []
    sollist = []
    freqlist = []
    f1list = []
    gradlist = []
    clusterlist = []

    f1Array = [50, 200, 400]
    gradArray = [200, 400, 600]
    clusterArray = [0, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    simu_count = len(f1Array)*len(gradArray)*iters

    print("Starting simulation - estimated time: {} hours ".format(simu_count+(5*len(clusterArray))/3600))
    for i, config in enumerate(list(itertools.product(f1Array, gradArray, clusterArray))*iters):
        print("Running iteration: {}/{}, f1: {}, grad: {}, clusters: {}".format(i+1, simu_count*len(clusterArray), config[0], config[1], config[2]))
        benchmark = [config[0] + config[1]*x for x in range(6)]
        np.savetxt('benchmark_frequencies.txt', benchmark, fmt = '%i')

        if (config[2] == 0):

            (bin, fbest, best) = algos.CMA_ratio(verbose=verbose, NGEN=5000, nVoxels=nVoxels, timeLimit=timeLimit, errorLimit=0.1)
            # bin = [2.808656126220426, 4.660962727729024, 2.3636172988154587, 3.316311270665622, 3.35142768510695, 3.7902972491483853, 2.753118039543312, 3.7380126576190693, 3.0384099695119975, 2.4737431008208124, 4.02632647695612, 3.109547093312928, 4.273884023468331, 3.1076252209040285, 3.340720386258119, 3.0881891242502855, 3.765003347867056, 4.301153775556621, 5.198151425485613, 3.3132885646634826, 3.009273859474627, 3.0395426477073593, 4.062077538371861, 2.9023028398810142, 3.388319545288303, 4.202841833941897, 2.952292743243537, 2.824184734723291, 2.5446150537640775, 3.802644074279686, 2.6881394215499967, 2.7523547947460187, 3.441620350125819, 3.9708299567397765, 2.384567331151244, 3.196860742812609, 4.615062661055728, 2.961349099370517, 3.0662807596891217, 3.0234206578153193]
            # fbest = [[5.282643763622793]]

            E = [10**(3*x) for x in bin]
            rho = [1e3]*40
            freq = blackbox.Elmer_blackbox_continuous(E, rho)

            bin_init = bin

        else:

            kmeans = KMeans(n_clusters=config[2])
            s_array = np.array(bin_init).reshape(-1, 1)
            kmeans.fit_predict(s_array) 
            s_labels = kmeans.labels_
            s_centers = kmeans.cluster_centers_
            avg_dis = np.sqrt(-kmeans.score(s_array)/40)

            rho_fake = [1e3]*nVoxels
            E_fake = [10**(3*s_centers[s_labels[x]][0]) for x in range(nVoxels)]
            bin = [np.log10(x) for x in E_fake]

            # print("bin = ", bin)
            # print("centers = ", s_centers)
            # print("E = ", E_fake)

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
    runHeuristic()
    # runHeuristic_c()
    # runKMeans()

if __name__ == "__main__":
	main()
