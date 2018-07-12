import math
from toolkit import *
import subprocess
import Elmer_benchmark
import re
from scipy import stats
import tempfile
import shutil
import os

from contextlib import contextmanager

# https://stackoverflow.com/a/24176022
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

global N
global goal

#Load benchmark goal from text file
from numpy import loadtxt
goal = loadtxt('benchmark_frequencies.txt')

N = 6
#NOTE - the generated mesh must match nVoxels for this to be useful
global nVoxels
nVoxels = 40

def blackbox_voxel(material_array, MPI = False, printToConsole = False):
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
    with tempfile.TemporaryDirectory() as tmpdirname:
        if printToConsole:
            print('Created temporary directory', tmpdirname)
        shutil.copy('40VoxelMesh.unv', tmpdirname)
        shutil.copy('ELMERSOLVER_STARTINFO', tmpdirname)
        shutil.copytree('Linear_mesh', tmpdirname+'/Linear_mesh')

        with cd(tmpdirname):

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
                    #print('Running ElmerSolver...\n')
                    subprocess.call('ElmerSolver > log.txt',shell=True)
            else: #Execute ElmerSolver_mpi
                if printToConsole == True:
                    subprocess.call('mpirun -np 8 ElmerSolver_mpi | tee log.txt',shell=True)
                else:
                    #print('Running ElmerSolver_mpi...\n')
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
    with tempfile.TemporaryDirectory() as tmpdirname:
        if printToConsole:
            print('Created temporary directory', tmpdirname)
        shutil.copy('40VoxelMesh.unv', tmpdirname)
        shutil.copy('ELMERSOLVER_STARTINFO', tmpdirname)
        shutil.copytree('Linear_mesh', tmpdirname+'/Linear_mesh')

        with cd(tmpdirname):
        
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
                    #print('Running ElmerSolver...\n')
                    subprocess.call('ElmerSolver > log.txt',shell=True)
            else: #Execute ElmerSolver_mpi
                if printToConsole == True:
                    subprocess.call('mpirun -np 8 ElmerSolver_mpi | tee log.txt',shell=True)
                else:
                    #print('Running ElmerSolver_mpi...\n')
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
    goal = loadtxt('benchmark_frequencies.txt')
    freq_goal = goal[:N]
    
    freq = blackbox_voxel(bin)

    fitness = 0
    for i in range(N):
        fitness += abs(freq[i] - freq_goal[i]) / freq_goal[i] * 100

    fitness = fitness/N

    return (fitness, )

def fitness_voxel_uniform(bin, goal_f1=None, goal_grad=None):
    
    freq = blackbox_voxel(bin)

    slope, intercept, r_value, p_value, std_err = stats.linregress(range(1, N+1), freq)
    penalty = 0

    # r_value approaches 1 as data is more linear
    if goal_f1:
        penalty = penalty + (abs(goal_f1 - slope - intercept)**2/goal_f1)
    if goal_grad:
        penalty = penalty + (abs(goal_grad - slope)/goal_grad)
    #fitness = -r_value**2 + (abs(goal_f1 - slope - intercept)/goal_f1)**2 + (abs(goal_grad - slope)/goal_grad)**2
    fitness = -r_value**2 * 3 + penalty

    return (fitness, )
    
def fitness_voxel_single(bin):
    goal = loadtxt('benchmark_frequencies.txt')
    freq_goal = goal[:N]
    
    freq = blackbox_voxel(bin)

    i = 3 - 1
    fitness = abs(freq[i] - freq_goal[i]) / freq_goal[i] * 100

    return (fitness, )

def fitness_voxel_continuous(bin):
    goal = loadtxt('benchmark_frequencies.txt')
    freq_goal = goal[:N]

    # Max because constraints don't work
    E = bin[0:40]
    E = [max(10**x, 1e6) for x in E]
    rho = bin[40:80]
    rho = [max(10**(x-6), 1e1) for x in rho]

    freq = Elmer_blackbox_continuous(E, rho)

    fitness = 0
    for i in range(N):
        fitness += abs(freq[i] - freq_goal[i]) / freq_goal[i] * 100

    fitness = fitness/N

    return (fitness, )

def fitness_voxel_continuous_KM(E, rho):
    goal = loadtxt('benchmark_frequencies.txt')
    freq_goal = goal[:N]

    freq = Elmer_blackbox_continuous(E, rho)

    fitness = 0
    for i in range(N):
        fitness += abs(freq[i] - freq_goal[i]) / freq_goal[i] * 100

    fitness = fitness/N

    return (fitness, freq)