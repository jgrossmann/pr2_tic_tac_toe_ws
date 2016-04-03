#!/usr/bin/env python

import cv2
import numpy as np
from matplotlib.pyplot import *


#img = cv2.blur(img,(11,11))
#img = cv2.blur(img,(11,11))
class ClusterLine():
	
	def __init__(self, xstart, xend, ystart, yend, clusterID):
		self.xstart = xstart
		self.xend = xend
		self.ystart = ystart
		self.yend = yend
		self.dist = self.lineMag()
		self.points = []
		self.id = clusterID
		
	def distanceToLine(self, point):
		return abs((self.yend - self.ystart)*point.x - (self.xend - self.xstart)*point.y + self.xend*self.ystart - self.yend*self.xstart) / self.dist
				
	def addPoint(self, point):
		self.points.append(point)

	def lineMag(self):
		return np.sqrt([(self.xend - self.xstart)**2 + (self.yend-self.ystart)**2])
		
	def update(self):
		xarr = np.empty([len(self.points)], dtype=int)
		yarr = np.empty([len(self.points)], dtype=int)
		
		index = 0
		for point in self.points:
			xarr[index] = point.x
			yarr[index] = point.y
			index += 1
		
		coeff = np.polyfit(xarr, yarr, 1)
		poly = np.poly1d(coeff)
		ys = poly(xarr)
		ylim([0, 3024])
		xlim([0, 4032])
		plot(xarr, yarr, 'o')
		plot([self.xstart, self.xend], [self.ystart, self.yend], 'x')
		plot(xarr, ys)
		
		
		maxY = max(ys)
		maxX = xarr[np.argmax(ys)]
		minY = min(ys)
		minX = xarr[np.argmin(ys)]
		
		#print(ys)
		plot([minX, maxX], [minY, maxY], 'x')
		show()
		self.xstart = minX
		self.xend = maxX
		self.ystart = minY
		self.yend = maxY
		
		self.points = []


		
		
class LineSegment():
	
	def __init__(self, point1, point2):
		self.point1 = point1
		self.point2 = point2
		self.slope = getSlope()
		
	def getSlope():
		if(self.point2.x - self.poin1.x == 0):
			return sys.maxint
		
		return ((self.point2.y - self.poin1.y) / (self.poin2.x - self.point1.x))
			
		
		
		
class Point():
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.cluster = -1
	
	def setCluster(self, cluster):
		self.cluster = cluster
	
def kmeans(rawPoints, width, height, epsilon):
	
	clusterLines = []
	clusterLines.append(ClusterLine(width/3, width/3, 0, height, 0))
	clusterLines.append(ClusterLine(2*width/3, 2*width/3, 0, height, 1))
	clusterLines.append(ClusterLine(0, width, height/3, height/3, 2))
	clusterLines.append(ClusterLine(0, width, 2*height/3, 2*height/3, 3))
	
	points = []
	x = []
	y = []
	lineSegments = []
	for x1, y1, x2, y2 in rawPoints[0]:
		points.append(Point(x1, y1))
		points.append(Point(x2, y2))
		lineSegments.append((Point(x1, y1), Point(x2, y2)))
		x.append(x1)
		x.append(x2)
		y.append(y1)
		y.append(y2)
		plot(x,y,'o')
	
	
	print('iteration 1')
	error = cluster(clusterLines, points)
	print(error)
	index = 2
	while(error > epsilon):
		print('iteration '+str(index))
		updateLines(clusterLines)
		error = cluster(clusterLines, points)
		print(error)
		index += 1
		
		
		
	
	return clusterLines
	
	
def getAverageSlopes(lineSegments):
	pass

def updateLines(lines):
	for line in lines:
		line.update()
	
	
	
def clusterSlopes(lineSegments):
	pass
	
def cluster(clusterLines, points):
	pointSwitches = 0
	
	for point in points:
	
		leastDist = 100000000
		for line in clusterLines:
		
			dist = line.distanceToLine(point)
			if(dist < leastDist):
				leastDist = dist
				bestLine = line
				
		bestLine.addPoint(point)
		
		if(bestLine.id != point.cluster):
			pointSwitches += 1
			point.cluster = bestLine.id
		
	return pointSwitches
	

def houghLinesProb(name):
	img = cv2.imread(name)
	img = sobel(name)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,50,150,apertureSize = 3)
	cv2.imwrite('cannylines.jpg', edges)
	minLineLength = 100
	maxLineGap = 10
	lines = cv2.HoughLinesP(edges,1,np.pi/180,80,minLineLength,maxLineGap)


	for x1,y1,x2,y2 in lines[0]:
		cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
		

	cv2.imwrite('houghlines2.jpg',img)
	
	print(len(img))
	print(len(img[0]))

	kmeans(lines, len(img[0]), len(img), 4)
	
	
def houghLines(name):
	img = cv2.imread(name)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,20,80,apertureSize = 3)

	lines = cv2.HoughLines(edges,1,np.pi/180,200)
	for rho,theta in lines[0]:
		a = np.cos(theta)
		b = np.sin(theta)
		x0 = a*rho
		y0 = b*rho
		x1 = int(x0 + 1000*(-b))
		y1 = int(y0 + 1000*(a))
		x2 = int(x0 - 1000*(-b))
		y2 = int(y0 - 1000*(a))
		
		
	cv2.line(img,(x1,y1),(x2,y2),(0,0,255), 2)
	cv2.imwrite('houghlines1.jpg',img)

def sobel(name):
	img = cv2.imread(name)
	img = cv2.blur(img, (25, 25))
	img = cv2.blur(img, (25, 25))
	#img = cv2.blur(img, (23, 23))
	#img = cv2.blur(img, (23, 23))
	#img = cv2.bilateralFilter(img, 9, 75, 75)
	sobelx8u = cv2.Sobel(img,cv2.CV_8U,1,0,ksize=5)
	sobely8u = cv2.Sobel(img,cv2.CV_8U,0,1,ksize=5)

	subplot(1,3,1), imshow(img,cmap = 'gray')
	title('Original'), xticks([]), yticks([])
	subplot(1,3,2), imshow(sobelx8u,cmap = 'gray')
	title('Sobel X CV_8U'), xticks([]), yticks([])
	subplot(1,3,3), imshow(sobely8u,cmap = 'gray')
	title('Sobel Y CV_8U'), xticks([]), yticks([])

	#show()
	return sobelx8u

if __name__ == '__main__':
	img = 'tictactoe.JPG'
	#houghLines(img)
	houghLinesProb(img)
	#sobel(img)
	
	
