from Point import *

class Cluster:
	def __init__(self, center):
		self.center = center
		self.points = []
		
	def update(self):
		xavg = 0
		yavg = 0
		for point in self.points:
			xavg += point.x
			yavg += point.y
		
		numPoints = len(self.points)
		if(numPoints == 0):
			self.center = Point(0, 0)
		else :
			xavg = int(xavg / len(self.points))
			yavg = int(yavg / len(self.points))
			self.center = Point(xavg, yavg)	
		
	def distance(self, point):
		return self.center.getDistance(point)
