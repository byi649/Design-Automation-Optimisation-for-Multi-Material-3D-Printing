import blackbox
import numpy as np
import operator
import multiprocessing

from deap import base
from deap import creator
from deap import tools
from deap import benchmarks
from deap import cma
from deap import algorithms

import random
from toolkit import *

import time

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

    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)

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

    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)

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

    # Generate a new population
    population = toolbox.population(n=40)
    # Evaluate the individuals
    fitnesses = toolbox.map(toolbox.evaluate, population)
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    for gen in range(NGEN):

        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        CXPB = 0.5
        MUTPB = 0.1
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

def GA_1(verbose=False, NGEN=250):

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

    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)

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

    # Generate a new population
    population = toolbox.population(n=40)
    # Evaluate the individuals
    fitnesses = toolbox.map(toolbox.evaluate, population)
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    for gen in range(NGEN):

        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        record = stats.compile(population)
        fbar = record['avg']
        fmin = record['min']

        k1 = 1.0
        k2 = 0.5
        k3 = 1.0
        k4 = 0.5
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            child1Changed = False
            child2Changed = False

            f1 = child1.fitness.values[0]
            f2 = child2.fitness.values[0]

            if (f1 < fbar):
                MUTPB1 = k2 * (f1 - fmin) / (fbar - fmin)
            else:
                MUTPB1 = k4

            if (f2 < fbar):
                MUTPB2 = k2 * (f2 - fmin) / (fbar - fmin)
            else:
                MUTPB2 = k4

            MUTPB1 += 0.05
            MUTPB2 += 0.05

            fdash = min(child1.fitness.values, child2.fitness.values)[0]
            if (fdash < fbar):
                CXPB = k1 * (fdash - fmin) / (fbar - fmin)
            else:
                CXPB = k3

            #print(fbar, fmin)
            #print(MUTPB1, MUTPB2, CXPB)

            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                child1Changed = True
                child2Changed = True

            if random.random() < MUTPB1:
                toolbox.mutate(child1)
                child1Changed = True

            if random.random() < MUTPB2:
                toolbox.mutate(child2)
                child2Changed = True

            if child1Changed:
                del child1.fitness.values
            if child2Changed:
                del child2.fitness.values

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

def PSO(verbose=False, NGEN=250):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Particle", list, fitness=creator.FitnessMin, speed=list, 
        smin=None, smax=None, best=None)

    def generate(size, pmin, pmax, smin, smax):
        part = creator.Particle(random.uniform(pmin, pmax) for _ in range(size)) 
        part.speed = [random.uniform(smin, smax) for _ in range(size)]
        part.smin = smin
        part.smax = smax
        return part

    def updateParticle(part, best, phi1, phi2):
        u1 = (random.uniform(0, phi1) for _ in range(len(part)))
        u2 = (random.uniform(0, phi2) for _ in range(len(part)))
        v_u1 = map(operator.mul, u1, map(operator.sub, part.best, part))
        v_u2 = map(operator.mul, u2, map(operator.sub, best, part))
        part.speed = list(map(operator.add, part.speed, map(operator.add, v_u1, v_u2)))
        for i, speed in enumerate(part.speed):
            if speed < part.smin:
                part.speed[i] = part.smin
            elif speed > part.smax:
                part.speed[i] = part.smax
        part[:] = list(map(operator.add, part, part.speed))
        if part[0] <= 0:
            part[0] = 1
        if part[1] <= 0:
            part[1] = 1

    toolbox = base.Toolbox()
    toolbox.register("particle", generate, size=2, pmin=1, pmax=1e13, smin=-1e13, smax=1e13)
    toolbox.register("population", tools.initRepeat, list, toolbox.particle)
    toolbox.register("update", updateParticle, phi1=2.0, phi2=2.0)
    toolbox.register("evaluate", blackbox.fitness2)

    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)

    pop = toolbox.population(n=40)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    logbook = tools.Logbook()
    logbook.header = ["gen", "evals"] + stats.fields

    # Objects that will compile the data
    fbest = np.ndarray((NGEN,1))
    xybest = np.ndarray((NGEN,2))

    best = None

    for g in range(NGEN):
        for part in pop:
            part.fitness.values = toolbox.evaluate((part[0], part[1]))
            if not part.best or part.best.fitness < part.fitness:
                part.best = creator.Particle(part)
                part.best.fitness.values = part.fitness.values
            if not best or best.fitness < part.fitness:
                best = creator.Particle(part)
                best.fitness.values = part.fitness.values
        for part in pop:
            toolbox.update(part, best)

        # Gather all the fitnesses in one list and print the stats
        logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
        if verbose:
            print(logbook.stream)

        fbest[g] = best.fitness.values
        xybest[g, :2] = [best[0], best[1]]
    
    return (xybest[g, 0], xybest[g, 1], fbest, xybest)

def GA_voxel(verbose=False, NGEN=10, nVoxels=4, nPop=40, timeLimit=float("inf"), errorLimit=1.0, crossover='ModalTwoPoint'):

    start = time.time()

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    # Attribute generator 
    toolbox.register("attr_bool", random.randint, 0, 1)
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, nVoxels)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", blackbox.fitness_voxel)

    if crossover == 'ModalTwoPoint':
        toolbox.register("mate", ModalTwoPoint)
    else:
        toolbox.register("mate", tools.cxTwoPoint)

    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)

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
    best = np.ndarray((NGEN, nVoxels))
    solutions = {}

    # Generate a new population
    population = toolbox.population(n=nPop)
    # Evaluate the individuals
    fitnesses = toolbox.map(toolbox.evaluate, population)
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit
        solutions[binaryToStr(ind)] = fit

    for gen in range(NGEN):   
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        CXPB = 0.5
        MUTPB = 0.1

        # Stop evolving when we reach a reasonable accuracy or time limit
        end = time.time()
        hof.update(offspring)
        if hof[0].fitness.values[0] > errorLimit and (end - start < timeLimit):
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

        else:
            if verbose:
                print("Skip generation:", gen)

        # Evaluate the individuals with an invalid fitness
        count = 0
        for ind in offspring:
            if ind.fitness.valid == False and binaryToStr(ind) in solutions:
                ind.fitness.values = solutions[binaryToStr(ind)]
                count += 1

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
            solutions[binaryToStr(ind)] = fit

        population[:] = offspring
        
        # Update the hall of fame and the statistics with the
        # currently evaluated population
        hof.update(population)
        record = stats.compile(population)
        logbook.record(evals=len(population), gen=gen, **record)
        
        if verbose:
            print(logbook.stream)
            print("Best solution:", hof[0])
            print("Number of fake evolutions:", count)
        
        # Save more data along the evolution for latter plotting
        fbest[gen] = hof[0].fitness.values
        best[gen, :nVoxels] = hof[0]


    return (hof[0], fbest, best)

def GA_voxel_uniform(verbose=False, NGEN=10, nVoxels=4, nPop=40, goal_f1=None, goal_grad=None):

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    # Attribute generator 
    toolbox.register("attr_bool", random.randint, 0, 1)
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, nVoxels)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", blackbox.fitness_voxel_uniform, goal_f1=goal_f1, goal_grad=goal_grad)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)

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
    best = np.ndarray((NGEN, nVoxels))
    solutions = {}

    # Generate a new population
    population = toolbox.population(n=nPop)
    # Evaluate the individuals
    fitnesses = toolbox.map(toolbox.evaluate, population)
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit
        solutions[binaryToStr(ind)] = fit

    for gen in range(NGEN):   
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        CXPB = 0.5
        MUTPB = 0.1

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
        count = 0
        for ind in offspring:
            if ind.fitness.valid == False and binaryToStr(ind) in solutions:
                ind.fitness.values = solutions[binaryToStr(ind)]
                count += 1

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
            solutions[binaryToStr(ind)] = fit

        population[:] = offspring
        
        # Update the hall of fame and the statistics with the
        # currently evaluated population
        hof.update(population)
        record = stats.compile(population)
        logbook.record(evals=len(population), gen=gen, **record)
        
        if verbose:
            print(logbook.stream)
            print("Best solution:", hof[0])
            print("Number of fake evolutions:", count)
        
        # Save more data along the evolution for latter plotting
        fbest[gen] = hof[0].fitness.values
        best[gen, :nVoxels] = hof[0]


    return (hof[0], fbest, best)

def GA_voxel_test(verbose=False, NGEN=10, nVoxels=4, nPop=40, timeLimit=float("inf"), errorLimit=1.0, crossover='ModalSixPoint'):

    start = time.time()

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    # Attribute generator 
    toolbox.register("attr_bool", random.randint, 0, 1)
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, nVoxels)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", blackbox.fitness_voxel)

    if crossover == 'ModalSixPoint':
        toolbox.register("mate", ModalSixPoint)
    else:
        toolbox.register("mate", tools.cxTwoPoint)

    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)

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
    best = np.ndarray((NGEN, nVoxels))
    solutions = {}

    # Generate a new population
    population = toolbox.population(n=nPop)
    # Evaluate the individuals
    fitnesses = toolbox.map(toolbox.evaluate, population)
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit
        solutions[binaryToStr(ind)] = fit

    for gen in range(NGEN):   
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        CXPB = 0.5
        MUTPB = 0.1

        # Stop evolving when we reach a reasonable accuracy or time limit
        end = time.time()
        hof.update(offspring)
        if hof[0].fitness.values[0] > errorLimit and (end - start < timeLimit):
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

        else:
            if verbose:
                print("Skip generation:", gen)

        # Evaluate the individuals with an invalid fitness
        count = 0
        for ind in offspring:
            if ind.fitness.valid == False and binaryToStr(ind) in solutions:
                ind.fitness.values = solutions[binaryToStr(ind)]
                count += 1

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
            solutions[binaryToStr(ind)] = fit

        population[:] = offspring
        
        # Update the hall of fame and the statistics with the
        # currently evaluated population
        hof.update(population)
        record = stats.compile(population)
        logbook.record(evals=len(population), gen=gen, **record)
        
        if verbose:
            print(logbook.stream)
            print("Best solution:", hof[0])
            print("Number of fake evolutions:", count)
        
        # Save more data along the evolution for latter plotting
        fbest[gen] = hof[0].fitness.values
        best[gen, :nVoxels] = hof[0]


    return (hof[0], fbest, best)

def hill_climbing(verbose=False, nVoxels=4, parallel=40, timeLimit=float("inf"), errorLimit=1.0):
    
    nVoxels=800

    # Generate random solution
    sol = list(np.random.randint(2, size=nVoxels))
    fitness = blackbox.fitness_voxel(sol)
    
    # Do sweeps
    # while(time < timeLimit and error > errorLimit):
    while(True):
        for i in range(nVoxels):
            temp_sol = sol.copy()
            temp_sol[i] = 1 - sol[i]
            temp_fitness = blackbox.fitness_voxel(temp_sol)

            if temp_fitness < fitness:
                fitness = temp_fitness
                sol = temp_sol.copy()

            print(fitness)
