# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.4.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/kzho956/Documents/Design-Automation-Optimisation-for-Multi-Material-3D-Printing')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

#Define beam dimensions
L = 100e-3 #Length of beam (x co-ord)
h = 20e-3 #height of beam (y co-ord)
b = 2e-3 #depth of beam (z co-ord)

#Number of voxels to use in x, y and z
nVoxel_x = 160

#Define characteristic voxel size
voxel_dx = L/nVoxel_x #fixing dy, dz for the time being

geompy = geomBuilder.New(theStudy)

#Defining co-ordinate system
O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)


#Create voxels as geometric blocks
Voxels = []
for i in range(nVoxel_x):
	Voxels.append(geompy.MakeBoxDXDYDZ(voxel_dx*(i+1), h,b))

#Generate cantilever geometry by partition with voxels
Partitioned_Cantilever = geompy.MakePartition(Voxels, [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)

#Explode shape and extract individual solids as voxels
Solids = geompy.ExtractShapes(Partitioned_Cantilever, geompy.ShapeType["SOLID"], True)

#Generate geometric groups for boundary and body index labelling purposes
Voxel_Volumes = []

for i in range(nVoxel_x):
	Voxel_Volumes.append(geompy.CreateGroup(Solids[i], geompy.ShapeType["SOLID"]))
	geompy.UnionIDs(Voxel_Volumes[-1], [1])

LHS_face = geompy.CreateGroup(Solids[0], geompy.ShapeType["FACE"])
geompy.UnionIDs(LHS_face, [3])



#Adding geometry to study
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )

for i in range(nVoxel_x):
	geompy.addToStudy( Voxels[i], 'Voxel_%i'%(i+1) )

geompy.addToStudy( Partitioned_Cantilever, 'Partitioned_Cantilever' )

for i in range(len(Solids)):
	geompy.addToStudyInFather( Partitioned_Cantilever, Solids[i], 'Solid_%i'%(i+1) )

for i in range(len(Solids)):
	geompy.addToStudyInFather( Solids[i], Voxel_Volumes[i], 'Voxel_%i_Vol'%(i+1) )

geompy.addToStudyInFather( Solids[0], LHS_face, 'LHS-face' )


###
### SMESH component
###

#Define characteristic dimensions of mesh elements
mesh_dx = 0.67e-3
import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
Mesh_1 = smesh.Mesh(Partitioned_Cantilever)
Regular_1D = Mesh_1.Segment()
Local_Length_1 = Regular_1D.LocalLength(mesh_dx,None,1e-07)
Quadrangle_2D = Mesh_1.Quadrangle(algo=smeshBuilder.QUADRANGLE)
Hexa_3D = Mesh_1.Hexahedron(algo=smeshBuilder.Hexa)
isDone = Mesh_1.Compute()

Voxel_Bodies = [] #Body groups for mesh
for i in range(nVoxel_x):
	Voxel_Bodies.append(Mesh_1.GroupOnGeom(Voxel_Volumes[i], 'Voxel_Body_%i'%(i+1),SMESH.VOLUME))

LHS_Boundary = Mesh_1.GroupOnGeom(LHS_face, 'LHS-boundary',SMESH.FACE)
#Voxel_Body_2 = Mesh_1.GroupOnGeom(Voxel_2_Vol,'Voxel_Body_2',SMESH.VOLUME)
#LHS_boundary = Mesh_1.GroupOnGeom(LHS_face,'LHS-boundary',SMESH.FACE)


## Set names of Mesh objects
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(Hexa_3D.GetAlgorithm(), 'Hexa_3D')
smesh.SetName(Quadrangle_2D.GetAlgorithm(), 'Quadrangle_2D')
smesh.SetName(Local_Length_1, 'Local Length_1')
smesh.SetName(LHS_Boundary, 'LHS-boundary')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')

for i in range(nVoxel_x):
	smesh.SetName(Voxel_Bodies[i], 'Voxel_Body_%i'%(i+1) )


#Export mesh as UNV file
try:
  Mesh_1.ExportUNV( r'/home/kzho956/Documents/Design-Automation-Optimisation-for-Multi-Material-3D-Printing/%i_Voxel_Mesh.unv'%(nVoxel_x) )
  pass
except:
  print 'ExportUNV() failed. Invalid file name?'

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
