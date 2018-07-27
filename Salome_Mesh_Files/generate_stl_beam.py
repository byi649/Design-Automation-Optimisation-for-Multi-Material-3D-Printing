# -*- coding: utf-8 -*-

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

#Define material array solution as bin
#0 - flexible, inclusions material
#1 - stiff, matrix material
bin = [0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0]

SF = 1000

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


geompy = geomBuilder.New(theStudy)

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

Voxels = []

Voxels.append(geompy.MakeBoxDXDYDZ(voxel_dx, voxel_dy, voxel_dz))
for i in range(len(bin)):
	if(bin[i] == 0):
		Voxels.append(geompy.MakeTranslation(Voxels[0], (i//nVoxel_y)*voxel_dx, (i%nVoxel_y)*voxel_dy,0))
		
del Voxels[0]

#Voxel2 = geompy.MakeTranslation(Voxel1, 20, 5, 0)
#Voxel3 = geompy.MakeTranslation(Voxel1, 40, 10, 0)
FusedVoxels = geompy.MakeFuseList(Voxels, True, True)
#[Solid_1,Solid_2,Solid_3] = geompy.ExtractShapes(FusedVoxels, geompy.ShapeType["SOLID"], True)
Matrix = geompy.MakeBoxDXDYDZ(120, 20, 4)
geompy.TranslateDXDYDZ(Matrix, -20, 0, 0)
#geompy.addToStudy( O, 'O' )
#geompy.addToStudy( OX, 'OX' )
#geompy.addToStudy( OY, 'OY' )
#geompy.addToStudy( OZ, 'OZ' )
#geompy.addToStudy( Voxel1, 'Voxel1' )
#geompy.addToStudy( Voxel2, 'Voxel2' )
#geompy.addToStudy( Voxel3, 'Voxel3' )
#geompy.addToStudy( FusedVoxels, 'FusedVoxels' )
#geompy.addToStudyInFather( FusedVoxels, Solid_1, 'Solid_1' )
#geompy.addToStudyInFather( FusedVoxels, Solid_2, 'Solid_2' )
#geompy.addToStudyInFather( FusedVoxels, Solid_3, 'Solid_3' )
#geompy.addToStudy( Matrix, 'Matrix' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
InclusionsMesh = smesh.Mesh(FusedVoxels)
NETGEN_1D_2D_3D = InclusionsMesh.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
isDone = InclusionsMesh.Compute()
MatrixMesh = smesh.Mesh(Matrix)
NETGEN_1D_2D_3D_1 = MatrixMesh.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
isDone = MatrixMesh.Compute()
try:
  InclusionsMesh.ExportSTL( os.getcwd() + '/InclusionMesh.stl' )
  pass
except:
  print 'ExportSTL() failed. Invalid file name?'
try:
  MatrixMesh.ExportSTL( os.getcwd() + '/MatrixMesh.stl' )
  pass
except:
  print 'ExportSTL() failed. Invalid file name?'


## Set names of Mesh objects
smesh.SetName(NETGEN_1D_2D_3D.GetAlgorithm(), 'NETGEN 1D-2D-3D')
smesh.SetName(InclusionsMesh.GetMesh(), 'InclusionsMesh')
smesh.SetName(MatrixMesh.GetMesh(), 'MatrixMesh')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
