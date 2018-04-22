import math
from toolkit import *
import subprocess
import re

global N
global goal
goal = [55.73843789146891, 348.21686728338096, 509.718646370548, 516.4824354644039, 974.5856546461372, 1561.7741652094128]

N = 6
#4 Voxel Model Solution: material_array = [PLA, Al, Al, PLA] = [0 1 1 0]
#f1[Hz]	=	56.87056214
#f2[Hz]	=	522.7659672
#f3[Hz]	=	637.69078
#f4[Hz]	=	656.4648486
#f5[Hz]	=	1306.01978
#f6[Hz]	=	2420.557282

def blackbox_4voxel(material_array, MPI = False, printToConsole = True):
	#Returns list of n natural frequencies for a FOUR voxel beam.
	
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
		#casefile.write('  Post File = eigen_results.vtu                     \n')
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
		casefile.write('  Name = "Polylactic Acid (PLA)"                    \n')
		casefile.write('  Mesh Poisson ratio = 0.35                         \n')
		casefile.write('  Poisson ratio = 0.35                              \n')
		casefile.write('  Youngs modulus = 3.5e9                            \n')
		casefile.write('  Density = 1.3e3                                   \n')
		casefile.write('End                                                 \n')
		casefile.write('                                                    \n')
		casefile.write('Material 2                                          \n')
		casefile.write('  Name = "Aluminium (generic)"                      \n')
		casefile.write('  Mesh Poisson ratio = 0.35                         \n')
		casefile.write('  Poisson ratio = 0.35                              \n')
		casefile.write('  Youngs modulus = 70e9                             \n')
		casefile.write('  Density = 2700                                    \n')
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
		casefile.write('  Name = "PLA Body Force"                           \n')
		casefile.write('  Stress Bodyforce 2 = $ -9.81 * 1.3e3              \n')
		casefile.write('End                                                 \n')
		casefile.write('                                                    \n')
		casefile.write('Body Force 2                                        \n')
		casefile.write('  Name = "Aluminium Body Force"                     \n')
		casefile.write('  Stress Bodyforce 2 = $ -9.81 * 2700               \n')
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

def blackbox(E, rho):
	#Returns vector of n natural frequencies[Hz] of a homogeneous cantilever beam with material properties:
	#E		Youngs Modulus [Pa]
	#rho	Density [kg/m3]

	printToConsole = False
	#MPI run will use 8 partitions
	MPI = True
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

    fitness = fitness/N

    return (fitness, )

def fitness_binary(bin):
    #goal = [55.73843789146891, 348.21686728338096, 509.718646370548, 516.4824354644039, 974.5856546461372, 1561.7741652094128]
    freq_goal = goal[:N]

    (E, rho) = binaryToVar(bin)
    
    freq = blackbox(E, rho*1e-6)
    fitness = 0
    for i in range(N):
        fitness += abs(freq[i] - freq_goal[i]) / freq_goal[i] * 100

    fitness = fitness/N

    return (fitness, )
    
def fitness_voxel(bin):
    freq_goal = goal[:N]
    
    freq = blackbox_4voxel(bin)

    fitness = 0
    for i in range(N):
        fitness += abs(freq[i] - freq_goal[i]) / freq_goal[i] * 100

    fitness = fitness/N

    return (fitness, )