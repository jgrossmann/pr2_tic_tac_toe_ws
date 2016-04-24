import math

class Point():
	
	def __init__(self, x, y):
		self.x = int(x)
		self.y = int(y)
	
	def getDistance(self, point2):
		xdif = point2.x - self.x
		ydif = point2.y - self.y
		return math.hypot(ydif, xdif)
		
	def __eq__(self, other):
		return (self.x == other.x and self.y == other.y)
		
	def inList(self, list):
		for point in list:
			if point == self:
				return True
		return False
