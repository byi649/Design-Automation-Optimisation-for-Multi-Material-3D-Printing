import blackbox
import numpy as np
import matplotlib.pyplot as plt
import algos
from toolkit import *

NGEN = 250
verbose = False

algorithm = "GA"

if algorithm == "GA":
    (E, fbest, best) = algos.GA(verbose, NGEN)
    (E, rho) = binaryToVar(E)
elif algorithm == "CMA":
    (E, rho, fbest, best) = algos.CMA(verbose, NGEN)

print("Best solution: E = {0:.3e}, rho = {1:.3e}".format(E, rho*1e-6))

freq = blackbox.blackbox(E, rho*1e-6)
print("Natural frequencies:")
print('\n'.join('{}: {} Hz'.format(*k) for k in enumerate(freq, 1)))

true_freq = [53.005922156059206, 332.20641980613505, 930.2811671037335, 1822.8783393540868, 3013.3294997485928, 4501.393450241724, 6287.070190833485, 8370.359721523866, 10751.262042312881, 13429.777153200515]

errors = []
for i in range(10):
    errors.append(abs(freq[i] - true_freq[i]) / true_freq[i] * 100)
errors = np.array(errors)

print("Average error: {0:.3e}%".format(np.average(errors)))

# The x-axis will be the number of evaluations
# Truncated at evaluation #2000 due to NaN shenanigans
x = list(range(0, 40 * NGEN, 40))
plt.figure()
plt.subplot(2, 2, 2)
plt.semilogy(x, fbest, "-c")
plt.grid(True)
plt.title("Average percentage error (log)")

ax = plt.gca()
ax.set_xlim(left=0, right=2000)

plt.subplot(2, 2, 1)
plt.plot(x, fbest, "-c")
plt.grid(True)
plt.title("Average percentage error")

ax = plt.gca()
ax.set_xlim(left=0, right=2000)

plt.subplot(2, 2, 3)
plt.plot(x, best)
plt.grid(True)
plt.title("Blue: E, orange: rho (*1e6)")

ax = plt.gca()
ax.set_xlim(left=0, right=2000)

plt.subplot(2, 2, 4)
plt.bar(x=range(1, 11), height=errors)
print(errors)
plt.title("Percentage error for each mode")

ax = plt.gca()
ax.set_ylim(bottom=min(errors)-np.std(errors), top=max(errors)+np.std(errors))

plt.show()