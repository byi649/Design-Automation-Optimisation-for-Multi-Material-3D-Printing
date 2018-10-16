#This script is to be imported using a working Salome installation to export a voxelised cantilever geometry in .unv format

###
### This file is generated automatically by SALOME v8.4.0 with dump python functionality
###

import sys,os
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, os.getcwd())

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

#Scale factor
SF = 1

#Define beam dimensions
L = SF*100e-3 #Length of beam (x co-ord)
h = SF*20e-3 #height of beam (y co-ord)
b = SF*4e-3 #depth of beam (z co-ord)

#Number of voxels to use in x, y and z
nVoxel_x = 10
nVoxel_y = 4
nVoxel_z = 1

#Define characteristic voxel size
voxel_dx = L/nVoxel_x 
voxel_dy = h/nVoxel_y
voxel_dz = b/nVoxel_z

#Define characteristic dimensions of mesh elements
mesh_dx = SF*0.67e-3


geompy = geomBuilder.New(theStudy)
#Global co-ordinate axes
O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

#Generate initial topology of untouched cantilever
Beam_Untouched = geompy.MakeBoxDXDYDZ(L, h, b)




#Generate planes for partitioning

#Length-wise partitioning (x-dirn)
Beam_Untouched_face_3 = geompy.GetSubShape(Beam_Untouched, [3])
Plane_1 = geompy.MakePlaneFace(Beam_Untouched_face_3, 100)
Beam_Untouched_edge_25 = geompy.GetSubShape(Beam_Untouched, [25])
Multi_Translation_1 = geompy.MakeMultiTranslation1D(Plane_1, Beam_Untouched_edge_25, voxel_dx, nVoxel_x)

#Height-wise partitioning (y-dirn)
Beam_Untouched_face_23 = geompy.GetSubShape(Beam_Untouched, [23])
Plane_2 = geompy.MakePlaneFace(Beam_Untouched_face_23, 100)
Beam_Untouched_edge_22 = geompy.GetSubShape(Beam_Untouched, [22])
Multi_Translation_2 = geompy.MakeMultiTranslation1D(Plane_2, Beam_Untouched_edge_22, voxel_dy, nVoxel_y)

#Depth-wise partitioning (z-dirn)
Beam_Untouched_face_31 = geompy.GetSubShape(Beam_Untouched, [31])
Plane_3 = geompy.MakePlaneFace(Beam_Untouched_face_31, 100)
Beam_Untouched_edge_20 = geompy.GetSubShape(Beam_Untouched, [20])
Multi_Translation_3 = geompy.MakeMultiTranslation1D(Plane_3, Beam_Untouched_edge_20, voxel_dz, nVoxel_z)


#Partition the geometry
Partitioned_Cantilever = geompy.MakePartition([Beam_Untouched], [Multi_Translation_1, Multi_Translation_2, Multi_Translation_3], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
Solids = geompy.ExtractShapes(Partitioned_Cantilever, geompy.ShapeType["SOLID"], True)

Voxel_Volumes = []
#Entity Labelling
for i in range(len(Solids)):
	#for j in range(nVoxel_y):
	Voxel_Volumes.append(geompy.CreateGroup(Solids[i], geompy.ShapeType["SOLID"]))
	geompy.UnionIDs(Voxel_Volumes[-1], [1])

geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Beam_Untouched, 'Beam_Untouched' )
geompy.addToStudyInFather( Beam_Untouched, Beam_Untouched_face_3, 'Beam_Untouched:face_3' )
geompy.addToStudy( Plane_1, 'Plane_1' )
geompy.addToStudyInFather( Beam_Untouched, Beam_Untouched_edge_25, 'Beam_Untouched:edge_25' )
geompy.addToStudy( Multi_Translation_1, 'Multi-Translation_1' )
geompy.addToStudy( Partitioned_Cantilever, 'Partitioned_Cantilever' )

for i in range(len(Solids)):
	geompy.addToStudyInFather( Partitioned_Cantilever, Solids[i], 'Solids_%i'%(i+1) )	
	geompy.addToStudyInFather( Solids[i], Voxel_Volumes[i], 'Voxel_%i_Vol'%(i+1) )

###
### SMESH component
###

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
for i in range(len(Voxel_Volumes)):
	Voxel_Bodies.append(Mesh_1.GroupOnGeom(Voxel_Volumes[i], 'Voxel_Body_%i'%(i+1),SMESH.VOLUME))

#Face group for fixed boundary of cantilever
aCriteria = []
aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,Plane_1)
aCriteria.append(aCriterion)
aFilter_1 = smesh.GetFilterFromCriteria(aCriteria)
aFilter_1.SetMesh(Mesh_1.GetMesh())
LHS_boundary = Mesh_1.GroupOnFilter( SMESH.FACE, 'LHS_boundary', aFilter_1 )

#LHS_Boundary = Mesh_1.GroupOnGeom(LHS_face, 'LHS-boundary',SMESH.FACE)
#Voxel_Body_2 = Mesh_1.GroupOnGeom(Voxel_2_Vol,'Voxel_Body_2',SMESH.VOLUME)
#LHS_boundary = Mesh_1.GroupOnGeom(LHS_face,'LHS-boundary',SMESH.FACE)


## Set names of Mesh objects
#smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
#smesh.SetName(Hexa_3D.GetAlgorithm(), 'Hexa_3D')
#smesh.SetName(Quadrangle_2D.GetAlgorithm(), 'Quadrangle_2D')
#smesh.SetName(Local_Length_1, 'Local Length_1')
#smesh.SetName(LHS_boundary, 'LHS-boundary')
#smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')

#for i in range(len(Voxel_Bodies)):
#	smesh.SetName(Voxel_Bodies[i], 'Voxel_Body_%i'%(i+1) )

#raise RuntimeError

#Export mesh as UNV file
try:
  Mesh_1.ExportUNV( os.getcwd() + '/Completed_mesh.unv' )
  pass
except:
  print 'ExportUNV() failed. Invalid file name?'


#if salome.sg.hasDesktop():
#  salome.sg.updateObjBrowser(True)
