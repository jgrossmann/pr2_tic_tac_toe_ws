from Point import *

class Cluster:
	def __init__(self, center):
		self.center = center
		self.points = []
		self.centerFound = False
		
	def update(self):
		xavg = 0
		yavg = 0
		for point in self.points:
			xavg += point.x
			yavg += point.y
		
		numPoints = len(self.points)
		if(numPoints == 0):
			return
		else :
			xavg = int(xavg / len(self.points))
			yavg = int(yavg / len(self.points))
			self.center = Point(xavg, yavg)	
			self.centerFound = True
		
	def distance(self, point):
		return self.center.getDistance(point)
