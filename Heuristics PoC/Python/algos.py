import blackbox
import numpy as np

from deap import base
from deap import creator
from deap import tools
from deap import benchmarks
from deap import cma
from deap import algorithms

import random
from toolkit import *

def CMA(verbose=False, NGEN=250):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0, ))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("evaluate", blackbox.fitness2)

    def feasible(individual):
        # Maximum bounds to catch NaN errors
        feasible = ((0 < individual[0] < 1e15) and (0 < individual[1] < 1e15))
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
    strategy = cma.Strategy(centroid=[5e9]*N, sigma=1e10, lambda_=20*N)
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

    # Objects that will compile the data
    fbest = np.ndarray((NGEN,1))
    best = np.ndarray((NGEN,N))

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


    return (hof[0][0], hof[0][1], fbest, best)

def GA(verbose=False, NGEN=250):

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    # Attribute generator 
    toolbox.register("attr_bool", random.randint, 0, 1)
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 100)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", blackbox.fitness_binary)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"

    # Objects that will compile the data
    fbest = np.ndarray((NGEN,1))
    best = np.ndarray((NGEN,2))

    for gen in range(NGEN):
        # Generate a new population
        population = toolbox.population(n=40)
        # Evaluate the individuals
        fitnesses = toolbox.map(toolbox.evaluate, population)
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit
        
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        CXPB = 0.5
        MUTPB = 0.2
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        population[:] = offspring
        
        # Update the hall of fame and the statistics with the
        # currently evaluated population
        hof.update(population)
        record = stats.compile(population)
        logbook.record(evals=len(population), gen=gen, **record)
        
        if verbose:
            print(logbook.stream)
        
        # Save more data along the evolution for latter plotting
        fbest[gen] = hof[0].fitness.values
        best[gen, :2] = binaryToVar(hof[0])


    return (hof[0], fbest, best)
