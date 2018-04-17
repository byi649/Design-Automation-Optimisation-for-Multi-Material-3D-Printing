import math
from toolkit import *
import subprocess
import re

global N
global ElementOrder
global goal

ElementOrder = 1
N = 6

if ElementOrder == 1:
	goal = [55.73843789146891, 348.21686728338096, 509.718646370548, 516.4824354644039, 974.5856546461372, 1561.7741652094128]
else:
	goal = [53.87447718322994, 336.5731957745863, 507.30722368970953, 516.099996928886, 941.7105318985997, 1552.129401103263]
	
# Inputs: Youngs modulus, density
# Output: List of first 6 natural frequencies of a cantilever with no load
def blackbox(E, rho):
	#Returns vector of n natural frequencies[Hz] of a homogeneous cantilever beam with material properties:
	#E		Youngs Modulus [Pa]
	#rho	Density [kg/m3]

	printToConsole = False
	#MPI run will use 8 partitions
	MPI = False
	#THIS ROUTINE MUST BE CALLED FROM AN ELMER WORKING DIRECTORY
	
	#Modify to change mesh/element order
	#ElementOrder = 1 for 13500 Element linear mesh, 2 for 4000 element quadratic mesh
	#ElementOrder = 1
	
	#Number of natural frequencies to solve for
	n = 6
	
	if ElementOrder == 1:
		meshDir = 'Linear_13500'
	else:
		meshDir = 'Quad_4000'
	
	with open('case.sif','w+') as casefile:
		casefile.write('Header\n')
		casefile.write('  CHECK KEYWORDS Warn\n')
		casefile.write(''.join(['Mesh DB "." "',meshDir,'"\n']))
		casefile.write('  Include Path ""\n')
		casefile.write('  Results Directory ""\n')
		casefile.write('End\n')
		casefile.write('\n')
		casefile.write('Simulation\n')
		casefile.write('  Coordinate System = Cartesian\n')
		casefile.write('  Coordinate Mapping(3) = 1 2 3\n')
		casefile.write('  Simulation Type = Steady state\n')
		casefile.write('  Steady State Max Iterations = 1\n')
		casefile.write('  Solver Input File = case.sif\n')
	#	casefile.write('  Post File = eigen_results.vtu\n') #Un-comment to write post-process file
		casefile.write('End\n')
		casefile.write('\n')
		casefile.write('Body 1\n')
		casefile.write('  Target Bodies(1) = 1\n')
		casefile.write('  Name = "Beam Volume"\n')
		casefile.write('  Equation = 1\n')
		casefile.write('  Material = 1\n')
		casefile.write('  Body Force = 1\n')
		casefile.write('End\n')
		casefile.write('\n')
		casefile.write('Solver 1\n')
		casefile.write('  Equation = "Stress Analysis"\n')
		casefile.write('  Eigen System Values = %i\n'%n)
		casefile.write('  Variable = "Displacement"\n')
		casefile.write('  Variable Dofs = 3\n')
		casefile.write('  Eigen System Select = Smallest magnitude\n')
		casefile.write('  Eigen Analysis = Logical True\n')
		casefile.write('  Steady State Convergence Tolerance = 1.0e-5\n')
		casefile.write('  Nonlinear System Convergence Tolerance = 1.0e-7\n')
		casefile.write('  Nonlinear System Max Iterations = 1\n')
		casefile.write('  Nonlinear System Newton After Iterations = 1\n')
		casefile.write('  Nonlinear System Newton After Tolerance = 1.0e-3\n')
		casefile.write('  Nonlinear System Relaxation Factor = 1\n')
		casefile.write('  Linear System Solver = Direct\n')
		casefile.write('  Linear System Direct Method = MUMPS\n')
		casefile.write('  Linear System Iterative Method = BiCGStab\n')
		casefile.write('  Linear System Max Iterations = 1\n')
		casefile.write('  Linear System Convergence Tolerance = 1.0e-5\n')
		casefile.write('  BiCGstabl polynomial degree = 2\n')
		casefile.write('  Linear System Preconditioning = Diagonal\n')
		casefile.write('  Linear System ILUT Tolerance = 1.0e-3\n')
		casefile.write('  Linear System Abort Not Converged = True\n')
		casefile.write('  Linear System Residual Output = 1\n')
		casefile.write('  Linear System Precondition Recompute = 1\n')
		casefile.write('End\n')
		casefile.write('\n')
		casefile.write('Equation 1\n')
		casefile.write('  Stress Analysis = True\n')
		casefile.write('End\n')
		casefile.write('\n')
		casefile.write('Material 1\n')
		casefile.write('  Name = "Polylactic Acid (PLA)"\n') #Placeholder name
		casefile.write('  Mesh Poisson ratio = 0.35\n') #Assume v = 0.35 - little influence on solutions for eigenmodes
		casefile.write('  Poisson ratio = 0.35\n')
		casefile.write('  Youngs modulus = %f\n' %E) #Youngs Modulus
		casefile.write('  Density = %f\n' %rho) #Density
		casefile.write('End\n')
		casefile.write('\n')
		casefile.write('\n')
		casefile.write('Body Force 1\n')
		casefile.write('  Name = "BodyForce 1"\n')
		casefile.write('  Stress Bodyforce 2 = $ -9.81 * %f\n' %rho) #gravity
		casefile.write('End\n')
		casefile.write('\n')
		casefile.write('Boundary Condition 1\n')
		casefile.write('  Target Boundaries(1) = 1\n')
		casefile.write('  Name = "fixed"\n')
		casefile.write('  Displacement 3 = 0\n')
		casefile.write('  Displacement 2 = 0\n')
		casefile.write('  Displacement 1 = 0\n')
		casefile.write('End\n')
	#print(MPI)	
	if MPI == True: #Execute ElmerSolver_mpi
		if printToConsole == True:
			subprocess.call('mpirun -np 8 ElmerSolver_mpi | tee log.txt',shell=True)
		else:
			print('Running ElmerSolver_mpi...\n')
			subprocess.call('mpirun -np 8 ElmerSolver_mpi > log.txt',shell=True)

	else: 
		#Execute ElmerSolver and output to log.txt
		if printToConsole == True:
			subprocess.call('ElmerSolver | tee log.txt',shell=True)
		else:
			print('Running ElmerSolver...\n')
			subprocess.call('ElmerSolver > log.txt',shell=True)
		
		

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

# Inputs: List of 10 frequencies, list of 10 goal frequencies
# Output: Fitness value (minimisation)
# Currently uses L2 norm
def fitness(freq, goal):
    #goal = [53, 332, 930, 1822, 3013, 4501, 6287, 8370, 10751, 13429]
    freq_goal = [int(a) for a in goal]
	
    fitness = 0
    for i in range(N):
        fitness += (freq[i] - freq_goal[i])**2

    fitness = math.sqrt(fitness/10)

    return fitness

# Input: List of [E, rho] where rho = true_rho * 1e6
# Output: Fitness value (minimisation)
# Fitness value is average percentage error
def fitness2(E):
    #goal = [55.73843789146891, 348.21686728338096, 509.718646370548, 516.4824354644039, 974.5856546461372, 1561.7741652094128]
    freq_goal = goal[:N]

    freq = blackbox(E[0], E[1]*1e-6)
    fitness = 0
    for i in range(N):
        fitness += abs(freq[i] - freq_goal[i]) / freq_goal[i] * 100

    fitness = fitness/10.

    return (fitness, )

def fitness_binary(bin):
    #goal = [55.73843789146891, 348.21686728338096, 509.718646370548, 516.4824354644039, 974.5856546461372, 1561.7741652094128]
    freq_goal = goal[:N]

    (E, rho) = binaryToVar(bin)
    
    freq = blackbox(E, rho*1e-6)
    fitness = 0
    for i in range(N):
        fitness += abs(freq[i] - freq_goal[i]) / freq_goal[i] * 100

    fitness = fitness/10.

    return (fitness, )

# Testing
# print(blackbox(3.5e9, 1.3e3))
# print(fitness(blackbox(3.5e9, 1.3e3), 1))
# print(fitness2(3.5e9, 1.3e9))
    
