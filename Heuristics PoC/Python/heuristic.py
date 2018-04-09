import blackbox
import numpy as np

from deap import base
from deap import creator
from deap import tools
from deap import benchmarks
from deap import cma
from deap import algorithms

creator.create("FitnessMin", base.Fitness, weights=(-1.0, ))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("evaluate", blackbox.fitness2)

def feasible(individual):
    # Maximum bounds to catch NaN errors
    feasible = ((0 < individual[0] < 1e15) and (0 < individual[1] < 1e10))
    return feasible

def distance(individual):
    # Distance from feasibility
    # Sum of distances from zero if negative
    distance = 0
    if individual[0] <= 0:
        distance += individual[0]
    if individual[1] <= 0:
        distance += individual[1]
    return -distance

# 1e11 chosen as greater than maximum potential objective value
toolbox.decorate("evaluate", tools.DeltaPenalty(feasible, 1e11, distance))

# Number of variables (E, rho -> 2)
N = 2

# Not sure if we can set individual sigma
# For now, scale rho down.
# TODO: Scale all variables down to unity
strategy = cma.Strategy(centroid=[5e9]*N, sigma=1e8, lambda_=20*N)
toolbox.register("generate", strategy.generate, creator.Individual)
toolbox.register("update", strategy.update)

hof = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("std", np.std)
stats.register("min", np.min)
stats.register("max", np.max)

algorithms.eaGenerateUpdate(toolbox, ngen=250, stats=stats, halloffame=hof)
print("Best solution: E = {0:.3e}, rho = {1:.3e}".format(hof[0][0], hof[0][1]*1e-6))

freq = blackbox.blackbox(hof[0][0], hof[0][1]*1e-6)
print("Natural frequencies:")
print('\n'.join('{}: {} Hz'.format(*k) for k in enumerate(freq, 1)))