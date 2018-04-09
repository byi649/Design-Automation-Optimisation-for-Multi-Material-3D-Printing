import blackbox
import numpy

from deap import base
from deap import creator
from deap import tools
from deap import benchmarks
from deap import cma
from deap import algorithms

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
#toolbox.register("evaluate", benchmarks.rastrigin)
toolbox.register("evaluate", blackbox.fitness2)

def feasible(individual):
    return individual[0] > 0

def distance(individual):
    """A distance function to the feasibility region."""
    return individual[0]**2

toolbox.decorate("evaluate", tools.DeltaPenalty(feasible, 1e3, distance))

N = 1

strategy = cma.Strategy(centroid=[5e9]*N, sigma=1e9, lambda_=20*N)
toolbox.register("generate", strategy.generate, creator.Individual)
toolbox.register("update", strategy.update)

hof = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

algorithms.eaGenerateUpdate(toolbox, ngen=250, stats=stats, halloffame=hof)
print(hof[0])