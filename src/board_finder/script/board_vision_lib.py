#!/usr/bin/env python

import cv2
import numpy as np
import math
from matplotlib.pyplot import *
from collections import defaultdict

angleRange = 5
		
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
		
	#def getAngleDif(self, line2):
	#	angle1 = self.getAngle()
	#	angle2 = line2.getAngle()
	#	
	#	dif = angle2 - angle1
	#	if(dif > math.pi):
	#		dif =  -(dif - math.pi)
	#	elif(dif < -math.pi):
	#		dif = -(dif + math.pi)
			
	#	return dif
		
				
		
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
		
	
class Square():
	def __init__(self, line, angle):
		self.top = None
		self.right = None
		self.bottom = None
		self.left = None
		self.setSides(line, angle)
		
	def setSides(self, line, angle):
		
		#case for neighbors being left and right
		if(angle >= 45):
			dist1 = line.point1.getDistance(line.neighbor1.point1)
			dist2 = line.point2.getDistance(line.neighbor1.point2)
			if(dist1 < dist2):
				pass
		
	def isFull(self):
		return (self.top != None and self.right != None
			and self.bottom != None and self.left != None)


class Board():
	def __init__(self, outersquare, innersquares):
		self.outline = outersquare
		centers = self.getSquareCenters(innersquares)
		if(len(centers) == 9):
			self.squareCenters = centers
		else :
			self.squareCenters = self.getOrderedCenters(centers)
		
	
	def getSquareCenters(self, squares):
		centers = []
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
					print('appending center '+str(x)+', '+str(y))
		
		return centers
		
		
	def getOrderedCenters(self, centers):
		line1 = LineSegment(Point(self.outline[0][0], self.outline[0][1]), 
			Point(self.outline[1][0], self.outline[1][1]))
		line2 = LineSegment(Point(self.outline[1][0], self.outline[1][1]),
			Point(self.outline[2][0], self.outline[2][1]))
		line3 = LineSegment(Point(self.outline[2][0], self.outline[2][1]),
			Point(self.outline[3][0], self.outline[3][1]))
		line4 = LineSegment(Point(self.outline[3][0], self.outline[3][1]),
			Point(self.outline[0][0], self.outline[0][1]))
		
		clusters = createClusters(line1, line2, line3, line4)
		
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
		
	
def createClusters(line1, line2, line3, line4):
	clusters = []
	
	ratio = 0.125
	dist1 = line1.point1.getDistance(line1.point2)
	dist2 = line3.point1.getDistance(line3.point2)
	distRatio = float(dist1 / dist2)
	
	height = line1.point1.getDistance(line4.point1)
	
	
	x = line1.point1.x
	y = line1.point1.y
	x += (line4.point1.x - line1.point1.x) * ratio
	x += (line2.point1.x - line1.point1.x) * ratio
	y += (line4.point1.y - line1.point1.y) * ratio
	y += (line2.point1.y - line1.point1.y) * ratio
	clusters.append(Cluster(Point(x, y)))
	
	x = int(np.mean([line1.point2.x, line1.point1.x]))
	y = int(np.mean([line1.point2.y, line1.point1.y]))
	x += (line4.point1.x - line1.point1.x) * ratio
	y += (line4.point1.y - line1.point1.y) * ratio
	clusters.append(Cluster(Point(x,y)))
	
	x = line1.point2.x
	y = line1.point2.y
	x += (line2.point2.x - line1.point2.x) * ratio
	x += (line1.point1.x - line1.point2.x) * ratio 
	y += (line2.point2.y - line1.point2.y) * ratio
	y += (line1.point1.y - line1.point2.y) * ratio 
	clusters.append(Cluster(Point(x,y)))
	
	x = int(np.mean([line4.point2.x, line4.point1.x]))
	y = int(np.mean([line4.point2.y, line4.point1.y]))
	x += (line2.point2.x - line4.point1.x) * ratio
	y += (line2.point2.y - line4.point1.y) * ratio
	y -= ((height/2.0) * (1 - distRatio))
	clusters.append(Cluster(Point(x,y)))
	
	x = np.mean([line1.point1.x, line2.point1.x, line3.point1.x, line4.point1.x])
	y = np.mean([line1.point1.y, line2.point1.y, line3.point1.y, line4.point1.y])
	y -= ((height/2.0) * (1 - distRatio))
	clusters.append(Cluster(Point(x,y)))
	
	x = int(np.mean([line2.point2.x, line2.point1.x]))
	y = int(np.mean([line2.point2.y, line2.point1.y]))
	x += (line4.point1.x - line2.point2.x) * ratio
	y += (line4.point1.y - line2.point2.y) * ratio
	y -= ((height/2.0) * (1 - distRatio))
	clusters.append(Cluster(Point(x,y)))
	
	x = line4.point1.x
	y = line4.point1.y
	x += (line1.point1.x - line4.point1.x) * ratio
	x += (line2.point2.x - line4.point1.x) * ratio
	y += (line1.point1.y - line4.point1.y) * ratio
	y += (line2.point2.y - line4.point1.y) * ratio
	y -= ((height/2.0) * (1 - distRatio))
	clusters.append(Cluster(Point(x,y)))
	
	x = int(np.mean([line3.point2.x, line3.point1.x]))
	y = int(np.mean([line3.point2.y, line3.point1.y]))
	x += (line1.point1.x - line3.point2.x) * ratio
	y += (line1.point1.y - line3.point2.y) * ratio
	y -= ((height/2.0) * (1 - distRatio))
	clusters.append(Cluster(Point(x,y)))
	
	x = line2.point2.x
	y = line2.point2.y
	x += (line1.point2.x - line2.point2.x) * ratio
	x += (line4.point1.x - line2.point2.x) * ratio
	y += (line1.point2.y - line2.point2.y) * ratio
	y += (line4.point1.y - line2.point2.y) * ratio
	y -= ((height/2.0) * (1 - distRatio))
	clusters.append(Cluster(Point(x,y)))
	
	return clusters		
	
	
	
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
	
		

def checkIntersection(a, b):
	A = np.polyfit([a[0][1], a[1][1]], [a[0][0], a[1][0]], 1)
	B = np.polyfit([b[0][1], b[1][1]], [b[0][0], b[1][0]], 1)

	x = (A[0] - B[0]) / (B[1] - A[1])
	assert np.around((A[0] * x + A[1]), 3) == np.around((B[0] * x + B[1]), 3)
	return x, (A[0] * x + A[1])

def find_func(x,y):
    return np.polyfit(x, y, 1)

def find_intersect(funcA, funcB):
    a = funcA[0]-funcB[0]
    b = funcB[1]-funcA[1]
    x = b / a 
    assert np.around(find_y(funcA,x),3) == np.around(find_y(funcB,x),3)
    return x, find_y(funcA,x)

def find_y(func, x):
    return func[0] * x + func[1]


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    contours = []
    for gray in cv2.split(img):
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
                b = cv2.Canny(gray, 50, 150, apertureSize=5)
                b = cv2.dilate(b, None)
            else:
                retval, b = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            	contours, hierarchy = cv2.findContours(b, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares





def houghLinesProb(name):
	squares = []
	img = cv2.imread(name)
	#img = sobel(name)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#cv2.imwrite('sobel.jpg', img)
	edges = cv2.Canny(gray,50,150,apertureSize = 3)
	cv2.imwrite('cannylines.jpg', edges)
	 
	contours, hierarchy = cv2.findContours(edges, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
	#print hierarchy
	
	for cnt in contours:
		cnt_len = cv2.arcLength(cnt, True)
		cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
		if len(cnt) == 4 and cv2.contourArea(cnt) > 20 and cv2.isContourConvex(cnt):
			cnt = cnt.reshape(-1, 2)
			max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
			if max_cos < 0.25:
				squares.append(cnt)
                      
                        
	#cv2.drawContours(img, squares, -1, (0, 255, 0), 1)
	
	print('outer')
	print(squares[15])
	outer, inner = isolateBoardSquares(squares)
	#board = Board(squares[15], squares[0:15])
	board = Board(outer, inner)
	
	
	#cv2.circle(img, (squares[15][0][0], squares[15][0][1]), 3, (0, 255, 0), -1)
	
	
	#cv2.imwrite('contours.jpg', img)
	
	for point in board.squareCenters:
		print(point.x, point.y)
		cv2.circle(img, (point.x, point.y), 3, (0, 255, 0), -1)
	cv2.imwrite('squarecenters.jpg', img)

	
	minLineLength = 50
	maxLineGap = 10
	cv2.imwrite('cannydilated.jpg', cv2.dilate(edges, None))
	lines = cv2.HoughLinesP(cv2.dilate(edges, None),1,np.pi/180,100,minLineLength,maxLineGap)

	for x1,y1,x2,y2 in lines[0]:
		cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)


	cv2.imwrite('houghlines2.jpg',img)

	
	
	#dst = cv2.cornerHarris(hough, 3, 3, 0.04)

	#dst = cv2.dilate(dst, None)

	#hough[dst>0.5*dst.max()] = [0, 0, 255]
	#cv2.imwrite('corners.jpg', hough)
	
	print(len(img))
	print(len(img[0]))
	
	return lines

	#kmeans(lines, len(img[0]), len(img), 4)
	
	
def houghLines(img):
	#img = cv2.imread(name)
	#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#edges = cv2.Canny(gray,20,80,apertureSize = 3)

	lines = cv2.HoughLines(img,1,np.pi/180,200)
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
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	img = cv2.blur(gray, (7, 7))
	#img = cv2.blur(img, (25, 25))
	#img = cv2.blur(img, (23, 23))
	#img = cv2.blur(img, (23, 23))
	#img = cv2.bilateralFilter(img, 9, 75, 75)
	sobelx8u = cv2.Sobel(img,cv2.CV_8U,1,0,ksize=5)
	sobely8u = cv2.Sobel(img,cv2.CV_8U,0,1,ksize=5)

	subplot(1,3,1), imshow(img,cmap = 'gray')
	title('Original'), xticks([]), yticks([])
	subplot(1,3,2), imshow(sobelx8u,cmap = 'gray')
	title('Sobel X CV_8U'), xticks([]), yticks([])
	subplot(1,3,3), imshow(sobely8u | sobelx8u,cmap = 'gray')
	title('Sobel Y CV_8U'), xticks([]), yticks([])

	show()
	return sobelx8u | sobely8u


def getIntersection(line1, line2):
	slope1 = line1.getSlope()
	slope2 = line2.getSlope()
	yInt1 =	line1.getYIntercept()
	yInt2 = line2.getYIntercept()
	
	if(slope1 == None):	
		assert slope2 != None
		x = line1.point1.x
		y = slope2*x + yInt2
	elif(slope2 == None):
		assert slope1 != None
		x = line2.point1.x
		y = slope1*x + yInt1
	else:
		x = float(yInt1 - yInt2) / float(slope2 - slope1)
		y = slope1*x + yInt1

	return x, y

def createLineMap(lines):
	map = defaultdict(list)
	
	for x1,y1,x2,y2 in lines[0]:
		line = LineSegment(Point(x1,y1), Point(x2, y2))
		map[line.getAngle()].append(line)
		
	return map
	
def getSquares(angleToLineMap):
	
	#lineMap = {};
	for angle, line in angleToLineMap:
		#if(lineMap[line] == None):
		
		angle = line.getAngle()
		if(angle >= 90):
			targetAngle = angle - 90
		else:
			targetAngle = angle + 90
			
		for index in range(targetAngle-angleRange, targetAngle+angleRange):
			lines = angleToLineMap[index]
			
			if(lines != None):
			
				for lineCandidate in lines:
					#if(lineMap[line] == None):
					dist1 = min(line.point1.getDistance(lineCandidate.point1), line.point1.getDistance(lineCandidate.point2))
					dist2 = min(line.point2.getDistance(lineCandidate.point1), line.point2.getDistance(lineCandidate.point2))
					
					if(dist1 < dist2):
						line.setNeighbor1(lineCandidate)
					else:
						line.setNeighbor2(lineCandidate)
						
		#lineMap[line.neighbor1] = line.neighbor1
		#lineMap[line.neighbor2] = line.neighbor2
		
		#set line with two neighbors into square
		square = Square(line, targetAngle)
			
	#iterate over map angle by angle
	#check for any lines at angles 90 degrees +/- 5 degrees in map
	#only take 2 lines that are closest to the line that are within degrees

def area(square):
	width = abs(square[1][0]  - square[0][0])
	length = abs(square[2][1] - square[1][1])
	return float(width * length)


def containsNineSquares(outersquare, squares):
	count = 0
	for square in squares:
		if(contains(outersquare, square)):
			count += 1
	if(count >= 9):
		return True
	else:
		return False
			

def contains(square1, square2):
	xtick = 0
	ytick = 0
	for point1 in square1:
		for point2 in square2:
			if(point2[0] > point1[0]):
				xtick += 1
			else:
				xtick -= 1
		
			if(point2[1] > point1[1]):
				ytick += 1
			else:
				ytick -= 1
		

	if((xtick == 0 and ytick <= 2) or (ytick == 0 and xtick <= 2)):
		return True
	
	return False

def isolateBoardSquares(squares):

	biggest = None
	index = 0
	for square in squares:
		size = area(square)
		
		if(biggest == None):
			biggest = (square, size, index)
		else:
			if(size > biggest[1]):
				biggest = (square, size, index)
				
		index += 1
		
	del squares[biggest[2]]
	print('biggest')
	print(biggest[0], biggest[1], biggest[2])
	if(len(squares) < 9):
		return None, None
		
	indexes = []
	if(containsNineSquares(biggest[0], squares) == False):
		return isolateBoardSquares(squares)
	else:
		index = 0
		for square in squares:
			if(contains(biggest[0], square) == False):
				indexes.append(index)
			index += 1
		print indexes
		for index in indexes:
			del squares[index]
			
		index = 0
		for square in squares:
			newSquares = squares[:]
			del newSquares[index]
			if(containsNineSquares(square, newSquares)):
				return isolateBoardSquares(squares)
			index += 1
			
		return biggest[0], squares
		

		
		


if __name__ == '__main__':
	img = 'kinect_image.png'
	#houghLines(img)
	lines = houghLinesProb(img)
	#sobel(img)
	#print(checkIntersection([[1, 1], [1, 2]], [[0, 2], [1, 2]]))
	#find fits
	
	image = cv2.imread(img)
	#squares = find_squares(image)
	#cv2.drawContours(image, squares, -1, (0, 255, 0), 3)
	#cv2.imwrite('squares.jpg', image)
	
	#want to get slopes or angles, make sure angle of lines are at about 90
	#degress +- 5 degrees
	line1 = LineSegment(Point(1,1), Point(1,2))
	line2 = LineSegment(Point(0,2), Point(1,2))
	
	print(getIntersection(line1, line2))
	print(line1.getAngle(), line2.getAngle())

	#angleToLineMap = createLineMap(lines)
	#print angleToLineMap

	#find intersection
	#x_intersect, y_intersect = find_intersect(func_A, func_B)
	#print(x_intersect, y_intersect)
	
