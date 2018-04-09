import math

# Inputs: Youngs modulus, density
# Output: List of first 10 natural frequencies of a cantilever with no load
def blackbox(E, rho):
    #E = 3.5e9
    #rho = 1.3e3
    w = 2e-3
    h = 2e-2
    L = 1e-1
    I = 1./12. * h * w**3
    A = w * h

    def alphaFormula(n):
        if n in range(4):
            alpha = [1.875, 4.694, 7.855, 10.996]
            return alpha[n - 1]
        return (2. * n - 1.) * math.pi / 2.

    alpha = []
    for i in range(10):
        alpha.append(alphaFormula(i + 1))

    freq = []
    for i in range(10):
        # Sometimes returns NaN ???
        freq.append(alpha[i]**2 / (2. * math.pi * L**2) * math.sqrt((E * I) / (rho * A)))
        # print(rho, A, rho*A)
        # print(alpha[i]**2 / (2. * math.pi * L**2) * math.sqrt((E * I) / (rho * A)))
        # print(E, I, rho, A)

    return freq

# Inputs: List of 10 frequencies, list of 10 goal frequencies
# Output: Fitness value (minimisation)
# Currently uses L2 norm
def fitness(freq, goal):
    goal = [53, 332, 930, 1822, 3013, 4501, 6287, 8370, 10751, 13429]
    fitness = 0
    for i in range(10):
        fitness += (freq[i] - goal[i])**2

    fitness = math.sqrt(fitness/10)

    return fitness

# Input: List of [E, rho] where rho = true_rho * 1e6
# Output: Fitness value (minimisation)
# Currently uses L2 norm
def fitness2(E):
    goal = [53.005922156059206, 332.20641980613505, 930.2811671037335, 1822.8783393540868, 3013.3294997485928, 4501.393450241724, 6287.070190833485, 8370.359721523866, 10751.262042312881, 13429.777153200515]
    freq = blackbox(E[0], E[1]*1e-6)
    fitness = 0
    for i in range(10):
        fitness += (freq[i] - goal[i])**2

    fitness = math.sqrt(fitness/10.)

    return (fitness, )

# Testing
# print(blackbox(3.5e9, 1.3e3))
# print(fitness(blackbox(3.5e9, 1.3e3), 1))
# print(fitness2(3.5e9))
    