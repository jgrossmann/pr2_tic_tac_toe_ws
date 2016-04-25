import numpy as np
import math

class LineSegment():
	
	def __init__(self, point1, point2):
		self.point1 = point1
		self.point2 = point2
		self.slope = None
		self.slope = self.getSlope()
		self.yInt = None
		self.yInt = self.getYIntercept()
		self.angle = None
		self.angle = self.getAngle()
		self.neighbor1 = None
		self.neighbor2 = None
		
	def getSlope(self):
		if(self.slope != None):
			return self.slope
			
		xdif = self.point2.x - self.point1.x
		ydif = self.point2.y - self.point2.y

		if(xdif == 0):
			return None
	
		return float(ydif / xdif)


	def getYIntercept(self):
		if(self.yInt != None):
			return self.yInt
			
		if(self.getSlope() == None):
			return None
			
		return float(self.point1.y - self.getSlope()*self.point1.x)	
		
	def getAngle(self):
		if(self.angle != None):
			return self.angle

		xdif = float(self.point2.x - self.point1.x)
		ydif = float(self.point2.y - self.point1.y)
		
		angle = math.atan2(ydif, xdif)
		if(angle < 0):
			angle = angle + math.pi
			
		return int(round(math.degrees(angle)))
		
	def setNeighbor1(self, line, dist):
		if(self.neighbor1 == None):
			self.neighbor1 = (line, dist)
			
		if(dist < self.neighbor1[1]):
			self.neighbor1 = (line, dist)
			
	def setNeighbor2(self, line, dist):
		if(self.neighbor2 == None):
			self.neighbor2 = (line, dist)
			
		if(dist < self.neighbor2[1]):
			self.neighbor2 = (line, dist)
		
	def getAngleDif(self, line2):
		angle1 = self.getAngle()
		angle2 = line2.getAngle()
		
		dif = angle2 - angle1
		if(dif > 180):
			dif =  (dif - 180)
		elif(dif < 0):
			dif = (dif + 180)
			
		return dif
