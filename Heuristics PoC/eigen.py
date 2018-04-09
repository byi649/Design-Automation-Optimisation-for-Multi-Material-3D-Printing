from fenics import *
from dolfin import *
import math
import numpy as np

import scipy.sparse as sp                                                       
from scipy.sparse.linalg import eigs   

moduli = [1e11]

# Create n different materials
# class K(Expression):
#     def set_k_values(self, k_array):
#         self.k_array = k_array
#     def eval(self, value, x):
#         # Cantilever is split into n materials serially along length
#         index = math.floor(x[0]*len(self.k_array))
#         value[0] = self.k_array[int(index)]

# Initialize kappa
# kappa = K(degree=0)
# kappa.set_k_values(moduli)

L = 100 # Length
W = 10 # Width
H = 1

#Young = kappa
Young = 1e11
poisson = 0.3

lambda_ = Young * poisson / ((1 + poisson) * (1 - 2*poisson))
mu = Young / (2 * (1 + poisson))

rho = 2330

# Create mesh and define function space
mesh = BoxMesh(Point(0, 0, 0), Point(L, W, H), 100, 3, 3)
V = VectorFunctionSpace(mesh, 'P', 1)

# Define boundary condition
tol = 1E-14

def clamped_boundary(x, on_boundary):
    return on_boundary and x[0] < tol

bc = DirichletBC(V, Constant((0, 0, 0)), clamped_boundary)

# Define strain and stress
def epsilon(u):
    return 0.5*(nabla_grad(u) + nabla_grad(u).T)
    #return sym(nabla_grad(u))

def sigma(u):
    return lambda_*nabla_div(u)*Identity(d) + 2*mu*epsilon(u)

# Define variational problem
u = TrialFunction(V)
d = u.geometric_dimension()  # space dimension
v = TestFunction(V)
f = Constant((0, 0, 0))
T = Constant((0, 0, 0))
a = inner(sigma(u), epsilon(v))*dx
L = dot(f, v)*dx + dot(T, v)*ds

m = inner(u, v) * dx    

# Assemble stiffness form
A = PETScMatrix()
#assemble(a, tensor=A)
#bc.apply(A)

M = PETScMatrix()                                                               
#assemble(m, tensor=M)                                                           

b = PETScVector()
assemble_system(a, L, bc, A_tensor=A, b_tensor=b)
assemble(m, M)

# This just converts PETSc to CSR                                               
A = sp.csr_matrix(A.mat().getValuesCSR()[::-1])                                 
M = sp.csr_matrix(M.mat().getValuesCSR()[::-1])

v, VV = eigs(A, 12, M, sigma=1, OPpart='r')                                                 

print(np.sqrt(v))
print(VV[:, 0])