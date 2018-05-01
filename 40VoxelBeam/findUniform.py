import algos
import blackbox
from scipy import stats
import matplotlib.pyplot as plt

NGEN = 10
verbose = True
nVoxels = 40

(bin, fbest, best) = algos.GA_voxel_uniform(verbose, NGEN, nVoxels)

print("Best solution:", bin)

freq = blackbox.blackbox_voxel(bin)
print("Natural frequencies:")
print('\n'.join('{}: {} Hz'.format(*k) for k in enumerate(freq, 1)))

slope, intercept, r_value, p_value, std_err = stats.linregress(range(6), freq)

print("Slope:", slope)
print("Intercept:", intercept)
print("r-squared:", r_value**2)

xind = range(6)
y = [intercept + x*slope for x in xind]

plt.bar(range(6), freq)
plt.plot(xind, y, 'r')
plt.show()