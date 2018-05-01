NGEN = 10
verbose = True
nVoxels = 40

(bin, fbest, best) = algos.GA_voxel_uniform(verbose, NGEN, nVoxels)

print("Best solution:", bin)

freq = blackbox.blackbox_voxel(bin)
print("Natural frequencies:")
print('\n'.join('{}: {} Hz'.format(*k) for k in enumerate(freq, 1)))