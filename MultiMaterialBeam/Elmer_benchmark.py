import subprocess
import math
import re

#NOTE - the generated mesh must match nVoxels for this to be useful
global nVoxels
nVoxels = 40
	
def Elmer_blackbox_voxels(material_array, MPI = False, printToConsole = False):
	#Returns list of n natural frequencies for a nVoxels beam.
	
	#Material array is a list of binary values
	#0	PLA plastic voxel
	#1	Generic Al alloy voxel

	#MPI run will use 8 partitions
	
	#THIS ROUTINE MUST BE CALLED FROM AN ELMER WORKING DIRECTORY
	
	#Modify to change mesh/element order
	#ElementOrder = 1 for 13500 Element linear mesh, 2 for 4000 element quadratic mesh
	#ElementOrder = 1
	
	#Number of natural frequencies to solve for
	n = 6
	
	meshDir = 'Linear_mesh'
	#if ElementOrder == 1:
	#	meshDir = 'Linear_13500'
	#else:
	#	meshDir = 'Quad_4000'
	
	with open('case.sif','w+') as casefile:
		casefile.write('Header                                              \n')
		casefile.write('  CHECK KEYWORDS Warn                               \n')
		casefile.write(''.join(['Mesh DB "." "',meshDir,'"\n']))
		casefile.write('  Include Path ""                                   \n')
		casefile.write('  Results Directory ""                              \n')
		casefile.write('End                                                 \n')
		casefile.write('                                                    \n')
		casefile.write('Simulation                                          \n')
		casefile.write('  Coordinate System = Cartesian                     \n')
		casefile.write('  Coordinate Mapping(3) = 1 2 3                     \n')
		casefile.write('  Simulation Type = Steady state                    \n')
		casefile.write('  Steady State Max Iterations = 1                   \n')
		casefile.write('  Solver Input File = case.sif                      \n')
		casefile.write('  Post File = eigen_results.vtu                     \n')
		casefile.write('End                                                 \n')
		casefile.write('                                                    \n')
		casefile.write('Solver 1                                            \n')
		casefile.write('  Equation = "Stress Analysis"                      \n')
		casefile.write('  Eigen System Values = %i                           \n' %n)
		casefile.write('  Variable = "Displacement"                         \n')
		casefile.write('  Variable Dofs = 3                                 \n')
		casefile.write('  Eigen System Select = Smallest magnitude          \n')
		casefile.write('  Eigen Analysis = Logical True                     \n')
		casefile.write('  Steady State Convergence Tolerance = 1.0e-5       \n')
		casefile.write('  Nonlinear System Convergence Tolerance = 1.0e-7   \n')
		casefile.write('  Nonlinear System Max Iterations = 1               \n')
		casefile.write('  Nonlinear System Newton After Iterations = 1      \n')
		casefile.write('  Nonlinear System Newton After Tolerance = 1.0e-3  \n')
		casefile.write('  Nonlinear System Relaxation Factor = 1            \n')
		casefile.write('  Linear System Solver = Direct                     \n')
		casefile.write('  Linear System Direct Method = MUMPS               \n')
		casefile.write('  Linear System Iterative Method = BiCGStab         \n')
		casefile.write('  Linear System Max Iterations = 1                  \n')
		casefile.write('  Linear System Convergence Tolerance = 1.0e-5      \n')
		casefile.write('  BiCGstabl polynomial degree = 2                   \n')
		casefile.write('  Linear System Preconditioning = Diagonal          \n')
		casefile.write('  Linear System ILUT Tolerance = 1.0e-3             \n')
		casefile.write('  Linear System Abort Not Converged = True          \n')
		casefile.write('  Linear System Residual Output = 1                 \n')
		casefile.write('  Linear System Precondition Recompute = 1          \n')
		casefile.write('End                                                 \n')
		casefile.write('                                                    \n')
		casefile.write('Equation 1                                          \n')
		casefile.write('  Stress Analysis = True                            \n')
		casefile.write('End                                                 \n')
		casefile.write('                                                    \n')
		casefile.write('Boundary Condition 1                                \n')
		casefile.write('  Target Boundaries(1) = 1                          \n')
		casefile.write('  Name = "fixed"                                    \n')
		casefile.write('  Displacement 3 = 0                                \n')
		casefile.write('  Displacement 2 = 0                                \n')
		casefile.write('  Displacement 1 = 0                                \n')
		casefile.write('End                                                 \n')
		casefile.write('                                                    \n')
		casefile.write('Material 1                                          \n')
		casefile.write('  Name = "Steelfill"                    \n')
		casefile.write('  Mesh Poisson ratio = 0.35                         \n')
		casefile.write('  Poisson ratio = 0.35                              \n')
		casefile.write('  Youngs modulus = 3.45e9                            \n')
		casefile.write('  Density = 2950                                   \n')
		casefile.write('End                                                 \n')
		casefile.write('                                                    \n')
		casefile.write('Material 2                                          \n')
		casefile.write('  Name = "Flex"                      \n')
		casefile.write('  Mesh Poisson ratio = 0.35                         \n')
		casefile.write('  Poisson ratio = 0.35                              \n')
		casefile.write('  Youngs modulus = 115e6                             \n')
		casefile.write('  Density = 1072.5                                    \n')
		casefile.write('End                                                 \n')
		casefile.write('                                                    \n')
		for i in range(len(material_array)): #Write material allocations for each voxel
			casefile.write('Body %i                                              \n'%(i+1))
			casefile.write('  Target Bodies(1) = %i                              \n'%(i+1))
			casefile.write('  Name = "Voxel_%i"                                  \n'%(i+1))
			casefile.write('  Equation = 1                                      \n')
			casefile.write('  Material = %i                                      \n'%(material_array[i]+1))
			casefile.write('  Body Force = %i                                    \n'%(material_array[i]+1))
			casefile.write('End                                                 \n')
			casefile.write('                                                    \n')
		casefile.write('Body Force 1                                        \n')
		casefile.write('  Name = "Steelfill Body Force"                           \n')
		casefile.write('  Stress Bodyforce 2 = $ -9.81 * 2950              \n')
		casefile.write('End                                                 \n')
		casefile.write('                                                    \n')
		casefile.write('Body Force 2                                        \n')
		casefile.write('  Name = "Flex Body Force"                     \n')
		casefile.write('  Stress Bodyforce 2 = $ -9.81 * 1072.5               \n')
		casefile.write('End                                                 \n')

	
	if MPI == False:
		#Execute ElmerSolver and output to log.txt
		if printToConsole == True:
			subprocess.call('ElmerSolver | tee log.txt',shell=True)
		else:
			print('Running ElmerSolver...\n')
			subprocess.call('ElmerSolver > log.txt',shell=True)
	else: #Execute ElmerSolver_mpi
		if printToConsole == True:
			subprocess.call('mpirun -np 8 ElmerSolver_mpi | tee log.txt',shell=True)
		else:
			print('Running ElmerSolver_mpi...\n')
			subprocess.call('mpirun -np 8 ElmerSolver_mpi > log.txt',shell=True)
		
		

	frequencies = []
	r = re.compile(r'[\s:]+')
	
	#Log file output differs slightly if MPI is used. Check for this
	if MPI == True:
		stringCheck = 'EigenSolve:            1'
		eigen_index = 3
	else:
		stringCheck = 'EigenSolve: 1:'
		eigen_index = 2
		
	#String split usage
	r = re.compile(r'[\s:]+')
	
	#Retrieve Eigenvalues from log.txt output
	with open('log.txt','r') as logfile:
		logfile.seek(0) #Return to start of logfile
		ln = logfile.readline().rstrip()
		#print(ln)
		while not ln.startswith(stringCheck):
			ln = logfile.readline().rstrip()
			#print(ln)
		for i in range(n):
			line = r.split(ln)
			frequencies.append(float(line[eigen_index]))
			ln = logfile.readline().rstrip()
		
	#Eigenvalues are omega^2. Convert to f [Hz] using omega = 2pi f
	frequencies = [(freq**0.5)/(2*math.pi) for freq in frequencies]
	
	#print(frequencies)
	return frequencies

def Elmer_blackbox_continuous(E_array, rho_array, MPI = False, printToConsole = False):
	#Returns list of n natural frequencies for an nVoxels voxel beam.
	
	#E_array List of size nVoxels containing YM allocated to voxel n
	#rho_array list of size nVoxels containing density allocated to voxel n

	#MPI run will use 8 partitions
	
	#THIS ROUTINE MUST BE CALLED FROM AN ELMER WORKING DIRECTORY
	
	#Modify to change mesh/element order
	#ElementOrder = 1 for 13500 Element linear mesh, 2 for 4000 element quadratic mesh
	#ElementOrder = 1
	
	#Number of natural frequencies to solve for
	n = 6
	
	meshDir = 'Linear_mesh'
	#if ElementOrder == 1:
	#	meshDir = 'Linear_13500'
	#else:
	#	meshDir = 'Quad_4000'
	
	with open('case.sif','w+') as casefile:
		casefile.write('Header                                              \n')
		casefile.write('  CHECK KEYWORDS Warn                               \n')
		casefile.write(''.join(['Mesh DB "." "',meshDir,'"\n']))
		casefile.write('  Include Path ""                                   \n')
		casefile.write('  Results Directory ""                              \n')
		casefile.write('End                                                 \n')
		casefile.write('                                                    \n')
		casefile.write('Simulation                                          \n')
		casefile.write('  Coordinate System = Cartesian                     \n')
		casefile.write('  Coordinate Mapping(3) = 1 2 3                     \n')
		casefile.write('  Simulation Type = Steady state                    \n')
		casefile.write('  Steady State Max Iterations = 1                   \n')
		casefile.write('  Solver Input File = case.sif                      \n')
		casefile.write('  Post File = eigen_results.vtu                     \n')
		casefile.write('End                                                 \n')
		casefile.write('                                                    \n')
		casefile.write('Solver 1                                            \n')
		casefile.write('  Equation = "Stress Analysis"                      \n')
		casefile.write('  Eigen System Values = %i                           \n' %n)
		casefile.write('  Variable = "Displacement"                         \n')
		casefile.write('  Variable Dofs = 3                                 \n')
		casefile.write('  Eigen System Select = Smallest magnitude          \n')
		casefile.write('  Eigen Analysis = Logical True                     \n')
		casefile.write('  Steady State Convergence Tolerance = 1.0e-5       \n')
		casefile.write('  Nonlinear System Convergence Tolerance = 1.0e-7   \n')
		casefile.write('  Nonlinear System Max Iterations = 1               \n')
		casefile.write('  Nonlinear System Newton After Iterations = 1      \n')
		casefile.write('  Nonlinear System Newton After Tolerance = 1.0e-3  \n')
		casefile.write('  Nonlinear System Relaxation Factor = 1            \n')
		casefile.write('  Linear System Solver = Direct                     \n')
		casefile.write('  Linear System Direct Method = MUMPS               \n')
		casefile.write('  Linear System Iterative Method = BiCGStab         \n')
		casefile.write('  Linear System Max Iterations = 1                  \n')
		casefile.write('  Linear System Convergence Tolerance = 1.0e-5      \n')
		casefile.write('  BiCGstabl polynomial degree = 2                   \n')
		casefile.write('  Linear System Preconditioning = Diagonal          \n')
		casefile.write('  Linear System ILUT Tolerance = 1.0e-3             \n')
		casefile.write('  Linear System Abort Not Converged = True          \n')
		casefile.write('  Linear System Residual Output = 1                 \n')
		casefile.write('  Linear System Precondition Recompute = 1          \n')
		casefile.write('End                                                 \n')
		casefile.write('                                                    \n')
		casefile.write('Equation 1                                          \n')
		casefile.write('  Stress Analysis = True                            \n')
		casefile.write('End                                                 \n')
		casefile.write('                                                    \n')
		casefile.write('Boundary Condition 1                                \n')
		casefile.write('  Target Boundaries(1) = 1                          \n')
		casefile.write('  Name = "fixed"                                    \n')
		casefile.write('  Displacement 3 = 0                                \n')
		casefile.write('  Displacement 2 = 0                                \n')
		casefile.write('  Displacement 1 = 0                                \n')
		casefile.write('End                                                 \n')
		casefile.write('                                                    \n')
		for i in range(nVoxels):
			#Write material definitions for each voxel
			casefile.write('Material %i                                          \n'%(i+1))
			casefile.write('  Name = "Voxel Material %i"                    \n'%(i+1))
			casefile.write('  Mesh Poisson ratio = 0.35                         \n')
			casefile.write('  Poisson ratio = 0.35                              \n')
			casefile.write('  Youngs modulus = %f                            \n'%(E_array[i]))
			casefile.write('  Density = %f                                   \n'%(rho_array[i]))
			casefile.write('End                                                 \n')
			#Write material allocations for each voxel
			casefile.write('Body %i                                              \n'%(i+1))
			casefile.write('  Target Bodies(1) = %i                              \n'%(i+1))
			casefile.write('  Name = "Voxel_%i"                                  \n'%(i+1))
			casefile.write('  Equation = 1                                      \n')
			casefile.write('  Material = %i                                      \n'%(i+1))
			casefile.write('  Body Force = %i                                    \n'%(i+1))
			casefile.write('End                                                 \n')
			casefile.write('                                                    \n')
			#Write body force definitions for each voxel
			casefile.write('Body Force %i                                        \n'%(i+1))
			casefile.write('  Name = "Voxel %i Body Force"                           \n'%(i+1))
			casefile.write('  Stress Bodyforce 2 = $ -9.81 * %f              \n'%(rho_array[i]))
			casefile.write('End                                                 \n')
	
	if MPI == False:
		#Execute ElmerSolver and output to log.txt
		if printToConsole == True:
			subprocess.call('ElmerSolver | tee log.txt',shell=True)
		else:
			print('Running ElmerSolver...\n')
			subprocess.call('ElmerSolver > log.txt',shell=True)
	else: #Execute ElmerSolver_mpi
		if printToConsole == True:
			subprocess.call('mpirun -np 8 ElmerSolver_mpi | tee log.txt',shell=True)
		else:
			print('Running ElmerSolver_mpi...\n')
			subprocess.call('mpirun -np 8 ElmerSolver_mpi > log.txt',shell=True)
		
		

	frequencies = []
	r = re.compile(r'[\s:]+')
	
	#Log file output differs slightly if MPI is used. Check for this
	if MPI == True:
		stringCheck = 'EigenSolve:            1'
		eigen_index = 3
	else:
		stringCheck = 'EigenSolve: 1:'
		eigen_index = 2
		
	#String split usage
	r = re.compile(r'[\s:]+')
	
	#Retrieve Eigenvalues from log.txt output
	with open('log.txt','r') as logfile:
		logfile.seek(0) #Return to start of logfile
		ln = logfile.readline().rstrip()
		#print(ln)
		while not ln.startswith(stringCheck):
			ln = logfile.readline().rstrip()
			#print(ln)
		for i in range(n):
			line = r.split(ln)
			frequencies.append(float(line[eigen_index]))
			ln = logfile.readline().rstrip()
		
	#Eigenvalues are omega^2. Convert to f [Hz] using omega = 2pi f
	frequencies = [(freq**0.5)/(2*math.pi) for freq in frequencies]
	
	#print(frequencies)
	return frequencies

from numpy import ones, zeros, savetxt, loadtxt
from numpy.random import randint

def generate_homogeneous_1(nVoxels): #Generate homogeneous test case for material 2
	material_array = ones(nVoxels)
	savetxt('material_array.txt',material_array, fmt = '%i')

	#return material_array

def generate_homogeneous_0(nVoxels): #Generate homogeneous test case for material 1
	material_array = zeros(nVoxels)
	savetxt('material_array.txt',material_array, fmt = '%i')

	#return material_array

def generate_random(nVoxels): #Generate a random text case
	material_array = randint(2,size = nVoxels)
	savetxt('material_array.txt',material_array, fmt = '%i')

	#return material_array

def generate_continuousArray(nVoxels): #Generate a homogeneous continuous test case
	E = 70e9
	rho = 2700.
	E_array = ones(nVoxels)*E
	rho_array = ones(nVoxels)*rho
	savetxt('elasticity_array.txt',E_array, fmt = '%.4f')
	savetxt('rho_array.txt',rho_array, fmt = '%.4f')

def generate_benchmark_soln(): #Generate solution from a material array
	material_array = loadtxt('material_array.txt',dtype = 'int')
	print('Generating benchmark solution for the following material_array:\n')
	print(material_array)
	print('\n')
	goal = Elmer_blackbox_voxels(material_array)
	print('The benchmark frequencies are:\n')
	print(goal)
	savetxt('benchmark_frequencies.txt',goal)

def generate_continuousSoln():
	E_array = loadtxt('elasticity_array.txt',dtype = 'float64')
	rho_array = loadtxt('rho_array.txt',dtype = 'float64')
	print('Generating benchmark solution for:\n')
	print('E = %f\n'%(E_array[0]))
	print('rho = %f\n'%(rho_array[0]))
	
	goal = Elmer_blackbox_continuous(E_array, rho_array,MPI=False, printToConsole=True)
	print('The benchmark frequencies are:\n')
	print(goal)
	savetxt('benchmark_frequencies.txt',goal)

def main():
	#generate_homogeneous_1(nVoxels)
	generate_homogeneous_0(nVoxels)
	#generate_random(nVoxels)
	generate_benchmark_soln()
	
	#generate_continuousArray(nVoxels)
	#generate_continuousSoln()

if __name__ == "__main__":
	main()
