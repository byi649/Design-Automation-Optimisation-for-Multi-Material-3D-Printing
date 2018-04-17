import subprocess
import math
import re

def Elmer_blackbox(E,rho, printToConsole = True):
	#Returns vector of SIX natural frequencies[Hz] of a homogeneous cantilever beam with material properties:
	#E		Youngs Modulus [Pa]
	#rho	Density [kg/m3]

	#THIS ROUTINE MUST BE CALLED FROM AN ELMER WORKING DIRECTORY
	
	#Modify to change mesh/element order
	#ElementOrder = 1 for 13500 Element linear mesh, 2 for 4000 element quadratic mesh
	ElementOrder = 1
	
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
	
	#Execute ElmerSolver and output to log.txt
	if printToConsole == True:
		subprocess.call('ElmerSolver | tee log.txt',shell=True)
	else:
		print('Running ElmerSolver...\n')
		subprocess.call('ElmerSolver > log.txt',shell=True)
		

	frequencies = []
	r = re.compile(r'[\s:]+')

	#Retrieve Eigenvalues from log.txt output
	with open('log.txt','r') as logfile:
		logfile.seek(0) #Return to start of logfile
		ln = logfile.readline().rstrip()
		print(ln)
		while not ln.startswith('EigenSolve: 1:'):
			ln = logfile.readline().rstrip()
			#print(ln)
		for i in range(n):
			line = r.split(ln)
			frequencies.append(float(line[2]))
			ln = logfile.readline().rstrip()
		
	#Eigenvalues are omega^2. Convert to f [Hz] using omega = 2pi f
	frequencies = [(freq**0.5)/(2*math.pi) for freq in frequencies]
	print(frequencies)
	return frequencies
	
#def retrieveFrequencies(logfile):
#	
#	#with open('log.txt','r') as logfile:
#	#	for line in logfile:
#	#		print(line.startswith('EigenSolve'))
#	##raise RuntimeError
#	#Retrieve Eigenvalues from log output
#	n = 6
#	frequencies = []
#	
#	r = re.compile(r'[\s:]+')
#
#	with open('log.txt','r') as logfile:
#		logfile.seek(0)
#		ln = logfile.readline().rstrip()
#		print(ln)
#		while not ln.startswith('EigenSolve: 1:'):
#			ln = logfile.readline().rstrip()
#			#print(ln)
#		for i in range(n):
#			line = r.split(ln)
#			frequencies.append(float(line[2]))
#			ln = logfile.readline().rstrip()
#		
#			
#	frequencies = [(freq**0.5)/(2*math.pi) for freq in frequencies]
#	return frequencies


#FOR DEBUGGING PURPOSES
def main():
	#PLA plastic parameters
	E = 3.5e9
	rho = 1.3e3
	Elmer_blackbox(E,rho,False)
	#frequencies = retrieveFrequencies('log.txt')
	#print(frequencies)

if __name__ == "__main__":
	main()