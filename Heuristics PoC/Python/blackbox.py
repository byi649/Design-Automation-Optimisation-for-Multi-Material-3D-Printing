import math

# Inputs: Youngs modulus, density
# Outputs: First 10 natural frequencies of a cantilever with no load
def blackbox(E, rho):
    #E = 3.5e9
    #rho = 1.3e3
    w = 2e-3
    h = 2e-2
    L = 1e-1
    I = 1/12 * h * w**3
    A = w * h

    def alphaFormula(n):
        if n in range(4):
            alpha = [1.875, 4.694, 7.855, 10.996]
            return alpha[n - 1]
        return (2 * n - 1) * math.pi / 2

    alpha = []
    for i in range(10):
        alpha.append(alphaFormula(i + 1))

    freq = []
    for i in range(10):
        freq.append(alpha[i]**2 / (2 * math.pi * L**2) * math.sqrt((E * I) / (rho * A)))

    return freq


# Testing
print(blackbox(3.5e9, 1.3e3))
    