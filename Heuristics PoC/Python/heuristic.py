import blackbox
import numpy as np
import matplotlib.pyplot as plt

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
strategy = cma.Strategy(centroid=[5e9]*N, sigma=1e9, lambda_=20*N)
toolbox.register("generate", strategy.generate, creator.Individual)
toolbox.register("update", strategy.update)

hof = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("std", np.std)
stats.register("min", np.min)
stats.register("max", np.max)

logbook = tools.Logbook()
logbook.header = "gen", "evals", "std", "min", "avg", "max"

NGEN = 250

# Objects that will compile the data
fbest = np.ndarray((NGEN,1))
best = np.ndarray((NGEN,N))

verbose = False
for gen in range(NGEN):
    # Generate a new population
    population = toolbox.generate()
    # Evaluate the individuals
    fitnesses = toolbox.map(toolbox.evaluate, population)
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit
    
    # Update the strategy with the evaluated individuals
    toolbox.update(population)
    
    # Update the hall of fame and the statistics with the
    # currently evaluated population
    hof.update(population)
    record = stats.compile(population)
    logbook.record(evals=len(population), gen=gen, **record)
    
    if verbose:
        print(logbook.stream)
    
    # Save more data along the evolution for latter plotting
    fbest[gen] = hof[0].fitness.values
    best[gen, :N] = hof[0]

print("Best solution: E = {0:.3e}, rho = {1:.3e}".format(hof[0][0], hof[0][1]*1e-6))

freq = blackbox.blackbox(hof[0][0], hof[0][1]*1e-6)
print("Natural frequencies:")
print('\n'.join('{}: {} Hz'.format(*k) for k in enumerate(freq, 1)))

# The x-axis will be the number of evaluations
# Truncated at evaluation #2000 due to NaN shenanigans
x = list(range(0, strategy.lambda_ * NGEN, strategy.lambda_))
plt.figure()
plt.subplot(2, 1, 1)
plt.semilogy(x, fbest, "-c")
plt.grid(True)
plt.title("Best objective function")

ax = plt.gca()
ax.set_xlim(left=0, right=2000)

plt.subplot(2, 1, 2)
plt.plot(x, best)
plt.grid(True)
plt.title("Blue: E, orange: rho (*1e6)")

ax = plt.gca()
ax.set_xlim(left=0, right=2000)

plt.show()