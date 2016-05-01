#!/usr/bin/env python

import cv2
import numpy as np
import math
from matplotlib.pyplot import *
from collections import defaultdict
from Board import *
from LineSegment import *
from Point import *
from Cluster import *

angleRange = 5				
			
	

		

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



def detectSquares(edges):
	squares = []
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
	#closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
	contours, hierarchy = cv2.findContours(edges, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
	print('num contours '+str(len(contours)))
	for cnt in contours:
		#print cnt
		cnt_len = cv2.arcLength(cnt, True)
		cnt = cv2.approxPolyDP(cnt, 0.025*cnt_len, True)
		if len(cnt) == 4 and cv2.contourArea(cnt) > 15 and cv2.isContourConvex(cnt):
			cnt = cnt.reshape(-1, 2)
			max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
			if max_cos < 0.5:
				squares.append(cnt)
				
	return squares



def detectBoard(img, name=None):

	if(name != None):
		img = cv2.imread(name)
	#img = sobel(name)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#cv2.imwrite('sobel.jpg', img)
	edges = cv2.Canny(gray,75,160,apertureSize = 3)
	cv2.imwrite('cannylines.jpg', edges)
	 
	temp = np.copy(edges)

	squares = detectSquares(temp)
                      
	if(squares == None):
		print('did not find any squares')
		return None

	imgcopy = np.copy(img)
	imgcopy2 = np.copy(img)
	imgcopy3 = np.copy(img)
 
	#kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
	#closed = cv2.morphologyEx(edges[:], cv2.MORPH_CLOSE, kernel)
	contours, hierarchy = cv2.findContours(edges, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)   
	      
	cv2.drawContours(img, squares, -1, (0, 255, 0), 2)
	cv2.imwrite('squares.jpg', img)
	

	outer, inner = isolateBoardSquares(squares)
	print('outer')
	print outer

	#board = Board(squares[15], squares[0:15])
	board = Board(outer, inner)
	print('board created')
	
	maxRad = 0
	if(board.innerSquares == None):
		return None
		
	for square in board.innerSquares:
		maxRad += getLongestDimension(square)
	maxRad = maxRad / len(board.innerSquares)
	maxRad = int((maxRad / 2) * 0.8)

	print 'max rad '+str(maxRad)
	
	#cv2.circle(img, (squares[15][0][0], squares[15][0][1]), 3, (0, 255, 0), -1)
	
	
	#cv2.imwrite('contours.jpg', img)
	
	
	for cluster in board.squareCenters:
		print(cluster.center.x, cluster.center.y)
		cv2.circle(img, (cluster.center.x, cluster.center.y), 3, (0, 255, 0), -1)
	cv2.imwrite('squarecenters.jpg', img)

	#try dilation if does not work well
	circles = cv2.HoughCircles(edges, cv2.cv.CV_HOUGH_GRADIENT, 1, maxRad, param1=60, param2=30, minRadius=3, maxRadius=maxRad)
	
	if(circles == None):
		print ("no circles found")
	else:

		circles = np.uint16(np.around(circles))
		for i in circles[0,:]:
			cv2.circle(imgcopy, (i[0], i[1]), i[2], (0, 255, 0), 2)
			cv2.circle(imgcopy, (i[0], i[1]), 2, (0, 0, 255), 3)
		
		board.setCircleLocations(circles, maxRad)
	
		cv2.imwrite('circles.jpg', imgcopy)
	
	
						
	#CREATE A BORDER AROUND BOARD WITH AT LEAST 2 PIXEL PADDING
	#THEN DO HOUGH LINES ON THAT PICTURE
	minLineLength = 6
	maxLineGap = 2
	cv2.imwrite('cannydilated.jpg', cv2.dilate(edges, None))
	lines = cv2.HoughLinesP(edges,1,np.pi/180,15,minLineLength,maxLineGap)

	for x1,y1,x2,y2 in lines[0]:
		cv2.line(imgcopy2,(x1,y1),(x2,y2),(0,255,0),2)


	cv2.imwrite('houghlines2.jpg',imgcopy2)
	
	xLocations = detectXs(board, lines, maxRad, imgcopy2)
	
	board.setXLocations(xLocations)

	

	

	return board
	#return centers, board.boardState

	

def detectXs(board, lines, maxRad, img):
	centers = board.getOpenCenters()
	centerMap = defaultdict(list)
	
	proximity = maxRad * .75
	
	xLocations = np.zeros(9)
	print(proximity)


	for x1,y1,x2,y2 in lines[0]:
		p1 = Point(x1, y1)
		p2 = Point(x2, y2)
	
		#print(p1.x, p1.y, p2.x, p2.y)
		for cluster, index in centers:
			
			#print(center.x, center.y)
			if(cluster.centerFound == False):
				if(p1.getDistance(cluster.center) <= maxRad or p2.getDistance(cluster.center) <= maxRad):
					centerMap[index].append(LineSegment(p1, p2))
			else:
				if(p1.getDistance(cluster.center) <= proximity or p2.getDistance(cluster.center) <= proximity):
					centerMap[index].append(LineSegment(p1, p2))
					break;
				
	#print(centerMap)
	minDist = 7
	minAngle = 41
	
	for center, lines in centerMap.iteritems():
		if(center == 7):
			for line in lines:
				cv2.line(img,(line.point1.x,line.point1.y),(line.point2.x, line.point2.y),(255, 0, 0),2)
	
	cv2.imwrite('x.jpg', img)
	
	for center, lines in centerMap.iteritems():
		if(center == 8):
			for line in lines:
				print(line.point1.x, line.point1.y, line.point2.x, line.point2.y)
		otherLines = lines[:]
		index = 0
		count = 0
		for line in lines:
			del otherLines[index]
			
			for otherLine in otherLines:
				if(line.point1.getDistance(otherLine.point1) <= minDist or
					line.point1.getDistance(otherLine.point2) <= minDist or
					line.point2.getDistance(otherLine.point1) <= minDist or
					line.point2.getDistance(otherLine.point2) <= minDist):
					
					if(line.getAngleDif(otherLine) > minAngle):
						count += 1
						if(count == 2):
							break;
						
			if(count == 2):
				break;
				
		if(count == 2):
			xLocations[center] = 2
			
	print('xlocations')
	print xLocations
	return xLocations
			
				
	
	
def getLongestDimension(square):
	p1 = Point(square[0][0], square[0][1])
	p2 = Point(square[1][0], square[1][1])
	p3 = Point(square[2][0], square[2][1])
	p4 = Point(square[3][0], square[3][1])
	
	dist = p1.getDistance(p2)
	dist = max(dist, p2.getDistance(p3))
	dist = max(dist, p3.getDistance(p4))
	dist = max(dist, p4.getDistance(p1))
	
	return dist
	
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
	arealimit = 10000
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
		
	if(biggest == None or biggest[1] < arealimit):
		return None, None
		
	del squares[biggest[2]]
	print('biggest')
	print(biggest[0], biggest[1], biggest[2])
	if(len(squares) < 9):
		return None, None
		
	indexes = []
	if(containsNineSquares(biggest[0], squares) == False):
		print('does not have 9 squares')
		return isolateBoardSquares(squares)
	else:
		index = 0
		for square in squares:
			if(contains(biggest[0], square) == False):
				indexes.append(index)
			index += 1
		print indexes

		tempSquares = []
		for i in range(0,len(squares)):
			if i not in indexes:
				tempSquares.append(squares[i])
				
			
		index = 0
		area 
		for square in tempSquares:
			newSquares = tempSquares[:]
			del newSquares[index]
			if(containsNineSquares(square, newSquares)):
				if(area(square) > arealimit):
					print 'another square contains nine'
					return isolateBoardSquares(tempSquares)
			index += 1
			
		return biggest[0], squares
		

		
		


if __name__ == '__main__':
	img = 'kinect_image.png'
	img = 'image.png'
	board = detectBoard(None, img)
	print board.boardState

	
