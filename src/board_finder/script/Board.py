import numpy as np
from board_vision import *

class Board():
	def __init__(self, outersquare, innersquares):
		self.outline = outersquare
		centers, self.innerSquares = self.getSquareCenters(innersquares)
		#if(len(centers) == 9):
		#	self.squareCenters = centers
		#else :
		self.squareCenters = self.getOrderedCenters(centers)
		self.boardState = np.zeros(9)
		
	
	def getSquareCenters(self, squares):
		centers = []
		pickedSquares = []
		if(squares == None):
			return None, None
			
		for square in squares:
			x = square[0][0] + square[1][0] + square[2][0] + square[3][0]
			x = int(x / 4)
			y = square[0][1] + square[1][1] + square[2][1] + square[3][1]
			y = int(y / 4)
			
			xtick = 0
			ytick = 0
			for point in self.outline:
				if(x > point[0]):
					xtick += 1
				else:
					xtick -= 1
				
				if(y > point[1]):
					ytick += 1
				else:
					ytick -= 1
				

			if((xtick == 0 and ytick <= 2) or (ytick == 0 and xtick <= 2)):
				if(Point(x,y).inList(centers) != True):	
					centers.append(Point(x,y))
					pickedSquares.append(square)
					print('appending center '+str(x)+', '+str(y))
		
		return centers, pickedSquares
		
		
	def getOrderedCenters(self, centers):
		if(self.outline == None):
			return None
			
		line1 = LineSegment(Point(self.outline[0][0], self.outline[0][1]), 
			Point(self.outline[1][0], self.outline[1][1]))
		line2 = LineSegment(Point(self.outline[1][0], self.outline[1][1]),
			Point(self.outline[2][0], self.outline[2][1]))
		line3 = LineSegment(Point(self.outline[2][0], self.outline[2][1]),
			Point(self.outline[3][0], self.outline[3][1]))
		line4 = LineSegment(Point(self.outline[3][0], self.outline[3][1]),
			Point(self.outline[0][0], self.outline[0][1]))
		
		clusters = createClusters(line1, line2, line3, line4)
		print('after clusters created')
		
		for center in centers:
		
			clusterIndex = 0
			curCluster = None
			
			for cluster in clusters:
				if(curCluster == None):
					curCluster = (clusterIndex, cluster.distance(center))
				else:
					dist = cluster.distance(center)
					if(dist < curCluster[1]):
						curCluster = (clusterIndex, dist)
						
				clusterIndex += 1
				
			clusters[curCluster[0]].points.append(center)
		
		self.clusters = clusters
		orderedCenters = []
		for cluster in clusters:
			cluster.update()
			orderedCenters.append(cluster.center)
			

		return orderedCenters
		
		
	def setCircleLocations(self, circles):
		openCenters = self.squareCenters[:]
		
		for i in circles[0,:]:
			p = Point(i[0], i[1])
			
			minDist = None
			index = 0
			for center in openCenters:
				dist = p.getDistance(center)
				if(minDist == None):
					minDist = (dist, index)
				else:
					if(dist < minDist[0]):
						minDist = (dist, index)
				index += 1
				
			self.boardState[minDist[1]] = 1
		print('boardstate')
		print self.boardState
		
		
	def setXLocations(self, locations):
	
		index = 0
		for value in locations:
			if(value == 2):
				if(self.boardState[index] == 0):
					self.boardState[index] = 2
			index += 1
		
		
	def getOpenCenters(self):
		centers = []
		index = 0;
		for i in self.boardState:
			if(i == 0):
				centers.append((self.squareCenters[index], index))
			index += 1
		return centers
			
