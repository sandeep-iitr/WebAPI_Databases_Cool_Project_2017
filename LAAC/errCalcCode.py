import numpy as np
from stl import mesh
import sys
import time
import math
import multiprocessing as mp
import tqdm


myError = 100000000
# Basic representation of an STL triangle
# Takes in 3-tuple of vertices and the normal vector
class Triangle(object):
	def __init__(self,vertices, normal):
		self.verts=vertices
		self.normal=normal/(np.sqrt(np.dot(normal,normal)))

class sliceParams(object):
	def __init__(self,obj,topheight,slice,density=10,local=0):
		self.obj=obj
		self.topheight=topheight
		self.slice=slice
		self.density=density
		self.local=local

# Representation of an entire STL object
# Takes in the name of the STL file (should be in same directory)
# Contains functionality for preprocessing the object triangles
# to make indexing by vertex position possible
class objectSTL(object):
	def __init__(self,model,angleX,angleY,angleZ):
		model.rotate([0.5, 0.0, 0.0], math.radians(angleX))
		model.rotate([0.0, 0.5, 0.0], math.radians(angleY))
		model.rotate([0.0, 0.0, 0.5], math.radians(angleZ))
		# Find the dimensions of the object
		vecs=model.vectors
		xmax=vecs[0][0][0]
		ymax=vecs[0][0][1]
		zmax=vecs[0][0][2]
		xmin=xmax
		ymin=ymax
		zmin=zmax
		for n in vecs:
			for m in n:
				if m[0] >xmax:
					xmax=m[0]
				if m[0] <xmin:
					xmin=m[0]
				if m[1] >ymax:
					ymax=m[1]
				if m[1] <ymin:
					ymin=m[1]
				if m[2] >zmax:
					zmax=m[2]
				if m[2] <zmin:
					zmin=m[2]
		Tris = []
		# Shift all our triangles to the z=0 level
		for i in range(0,len(model.vectors)):
			Tris.append(Triangle(model.vectors[i] - np.array([[xmin,ymin,zmin],[xmin,ymin,zmin],[xmin,ymin,zmin]]),model.normals[i]))
		xmax=xmax-xmin+.0001
		xmin=0.0001
		ymax=ymax-ymin+.0001
		ymin=0.0001
		zmax=zmax - zmin+.0001
		zmin=0.0001
		W=abs(xmax-xmin)
		L=abs(ymax-ymin)
		self.xmin=xmin
		self.ymin=ymin
		self.zmin=zmin
		self.xmax=xmax
		self.ymax=ymax
		self.zmax=zmax
		self.Tris=Tris
		self.width=xmax-xmin
		self.length=ymax-ymin
		self.height=zmax-zmin
		self.X=[[] for i in range(int(round(self.width+0.5)))]
		self.Y=[[] for i in range(int(round(self.length+0.5)))]
		self.Z=[[] for i in range(int(round(self.height+1.5)))]	
		self.preprocess()
	
	def preprocess(self):
		for ind,t in enumerate(self.Tris):
			xmin=t.verts[0][0]
			ymin=t.verts[0][1]
			zmin=t.verts[0][2]
			xmax=xmin
			ymax=ymin
			zmax=zmin
			for v in t.verts:
				if v[0] < xmin:
					xmin=v[0]
				if v[1] < ymin:
					ymin=v[1]
				if v[2] < zmin:
					zmin=v[2]
				if v[0] > xmax:
					xmax=v[0]
				if v[1] > ymax:
					ymax=v[1]
				if v[2] > zmax:
					zmax=v[2]
			for i in range(int(round(xmin-self.xmin)),int(round(xmax-self.xmin))):
				self.X[i].append(ind)
			for i in range(int(round(ymin-self.ymin)),int(round(ymax-self.ymin))):
				self.Y[i].append(ind)
			for i in range(int(round(zmin-self.zmin)),int(round(zmax-self.zmin)+1)):
				self.Z[i].append(ind)
	


# Computes the error of a single slice of a given object
# at a given height
# Takes in the object (as objectSTL), the height, the slice 
# width, and the desired accuracy in the form of grid points
# per mm^2 (higher is more accurate, but will increase 
# processing time)
# Should guarantee 
def sliceError( obj, topheight, slice,density,local=0):
	pts=[]
	width=obj.width
	length=obj.length
	m=int(width*density)
	n=int(length*density)
	# This is how much area there is per point
	ptDensity=width*length/(m*n)
	gridvol=ptDensity*25
	error = 0
	# - Construct the grid of points to use
	for i in range(0,m):
		for j in range(0,n):
			pts.append((obj.xmin+(width/m)*(0.5+i),obj.ymin+(length/n)*(0.5+j),topheight))
	localgrid = [[0 for i in range(int(m/5))] for j in range(int(n/5))]
	# For each of point, triangles considered will be the set intersection of the X,Y, and Z sets 
	# Get the index set of relevant triangles for this slice (Z)
	zset=set()
	for i in range(max(int(topheight-slice),0),int(topheight)+1):
		zset=zset.union(set(obj.Z[i]))
	total=len(pts)
	ptnum=1
	# - For each point:
	for pt in pts:
		#print(str(round((ptnum/total)*100)) + '%',end='\r')
		# Create a ray to a point *definitely* outside the object (it's outside the whole range)
		ray=(np.array(pt), np.array((obj.xmin-width*.1,obj.ymin-length*.1,topheight-slice*0.1)))
		down=(np.array(pt), np.array((pt[0],pt[1],pt[2]-slice)))
		inters=0
		# Compute the inside-ness and simultaneously compute amount of segment
		# that is in the outside, and amount that is in the inside
		# Further narrow down the list of triangles with X & Y
		xset=set(obj.X[int(pt[0])])
		yset=set(obj.Y[int(pt[1])])
		relevantTris=xset.intersection(yset.intersection(zset))
		errorlengths=[]
		#print(pt)
		for t in relevantTris:
			tr=obj.Tris[t]
			#print(tr.verts)
			interlength = edgeDetect(tr,ray)
			errorlength = edgeDetect(tr,down)
			if interlength > 0:
				inters = inters + 1
			if errorlength > 0:
				# For some reason, sometimes this will be the entire thickness.
				# However, this is practically impossible so it is ignored
				#print(errorlength)
				if abs(errorlength-slice) >= 0.00001:
					i=errorlength*np.sign(np.dot(tr.normal,down[1]-down[0])/(np.linalg.norm(tr.normal)*np.linalg.norm(down[1]-down[0])))
					errorlengths.append(i)
					#localgrid[int(((m/width)*(pt[0]-obj.xmin)-0.5)/5)][int(((n/length)*(pt[1]-obj.ymin))/5)] += i
		# 4 cases: the initial point is inside/outside * there are even/odd num of intersections
		# inside, even: negative sum of intersections
		# inside, odd: negative sum of intersections + slice thickness
		# outside, even: sum of intersections
		# outside, odd: sum of intersections + slice thickness
		# Note: outside if num of inters % 2 is 0
		#       even if num of downinters % 2 is 0
		outside = (inters % 2 == 0)
		suminters=sum(errorlengths)
		curerrorlength = suminters*-((inters%2)*2-1) + (len(errorlengths)%2)*slice
		# Add the appropriate error
		error = error + curerrorlength*ptDensity
		ptnum=ptnum+1
	if local > 0:
		for i in range(int(m/5)):
			for j in range(int(n/5)):
				if localgrid[i][j]/gridvol >= local*gridvol:
					print(localgrid[i][j]/gridvol)
					print(local*gridvol)
					return -1
	return error

def SPSE(s):
	return sliceError(s.obj,s.topheight,s.slice,s.density,s.local)

# Implements the Moller-Trumbore algorithm to compute
# distance that a ray intersects a triangle at
def edgeDetect(tri,ray):
		v0=tri.verts[0]
		v1=tri.verts[1]
		v2=tri.verts[2]
		p0=ray[0]
		p1=ray[1]
		V=p1-p0
		D=np.linalg.norm(V)
		if (D == 0):
			return 0
		# Use epsilon to increase tolerance at edge cases (when intersection point is ON the plane)
		# Define it as a small proportion of the segment length
		epsilon = D*0.01
		V=V/D
		T=p0-v0
		E1=v1-v0
		E2=v2-v0
		Q=np.cross(T,E1)
		P=np.cross(V,E2)
		if (abs(np.dot(P,E1)) < .0001):
			return 0
		sol=np.array([np.dot(Q,E2),np.dot(P,T),np.dot(Q,V)])/np.dot(P,E1)
		t=sol[0]
		u=sol[1]
		v=sol[2]
		if (u > 0 and u < 1 and v > 0 and v < 1 and u+v < 1 and t > -epsilon  and t < D+epsilon):
			return t
		return 0

# Just calls the slice error function on each slice
# and sums up the error
# Takes in the object, the uniform thickness, and
# optionally the density. Density is set to 10 by
# default as a reasonable value
def calculateError(obj, thickness, density=10):
	log=time.time()
	slices=math.ceil(obj.height/thickness)
	thicknesses=[thickness for i in range(slices)]
	totalError=0
	height=obj.height
	sl=range(slices)
	params=[]
	for i,t in enumerate(thicknesses):
		params.append(sliceParams(obj,height,t,density))
		#print(err)
		height=height-t
	result=[]
	p=mp.Pool()
	for r in tqdm.tqdm(p.imap_unordered(SPSE, params), total=len(params),ncols=50):
		result.append(r)
		pass
	totalError=sum(result)
	print('Time Elapsed: ' + str(time.time()-log))
	print('Total staircase error: '+str(totalError)) 
	errorMetric=math.sqrt(slices) * totalError

	global myError
	myError = errorMetric
	print('Error Metric: ' + str(errorMetric))
	return totalError
def main():

	myMin = 100000000
	bestX = 0
	bestY = 0
	global myError

	
	for i in range (350, 370, 1):
		model = mesh.Mesh.from_file("SimpleLion.stl")	
		stlObj=objectSTL(model, i, 183, 0) #change angleX, angleY, angleZ to the values to want
		calculateError(stlObj,0.2,5)
		if(myError < myMin):
			myMin = myError
			bestX = i
			bestY = 183

	print(bestX, bestY, myError)
	print("END")
if __name__ == "__main__": main()
