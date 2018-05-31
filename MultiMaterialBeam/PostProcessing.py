import numpy as np
from matplotlib import pyplot as plt

def PlotMaterialArray(MaterialArray,nx,ny,nz):
	#Re-shapes a 1D material array of voxel allocations into a 3D array shape for plotting corresponding to nx ny and nz no. of voxels in the respective directions
	fig, ax = plt.subplots(nz,1)
	#ax.plot(x, y)
	#ax.set_title('Simple plot')
	#plt.text(0,-40,'Voxel allocation in cantilever: Yellow = Al, Purple = PLA',fontsize=16)
	for i in range(nz):
		Slice = MaterialArray[i::nz]
		Slice = Slice.reshape((nx,ny)).T
        #plt.title("Beam voxels: yellow = AL, purple = PLA")
        #plt.axis("off")
		ax[i].imshow(Slice)
		ax[i].set_title('Voxel allocation for slice %i'%(i+1))
		ax[i].set_yticklabels([])
		ax[i].set_xticklabels([])
	fig.suptitle('Voxel allocation in cantilever: Yellow = Al, Purple = PLA\n nX = %i, nY = %i, nZ = %i, nVoxels = %i'%(nx,ny,nz,nx*ny*nz),fontsize=16)
	plt.show(fig)
def main():
	#800 voxel sample case
	material_array = np.loadtxt('material_array.txt',dtype = 'int')
	PlotMaterialArray(material_array,40,10,2)
if __name__ == "__main__":
	main()