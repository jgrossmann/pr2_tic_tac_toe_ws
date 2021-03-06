#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
import board_vision
from board_finder.msg import Kinect_Image
from board_finder.msg import TicTacToe
from Board import *
from TTT import *

publisher = None  #publishes vision data to AI
lastBoard = None  #lastBoard sent from vision

#gets the x y and z coordinate arrays from the xyz message array
def getWorldCoordinates(centers, coordinates, width):
	x = [];
	y = [];
	z = [];
	for center in centers:
		index = center.y * (width * 3) + (center.x * 3)
		x.append(coordinates[index])
		y.append(coordinates[index+1])
		z.append(coordinates[index+2])

		
	return x,y,z


#callback from receiving transformed kinect message
def callback(data):
	global lastBoard
	
	bridge = CvBridge()
	
	try:
		img = bridge.imgmsg_to_cv2(data.rgb, "rgb8")
		
	except CvBridgeError as e:
		print(e)
		
	'''
	try:
		cv2.imwrite('image.png', img)
	except:
		print("Error writing image")
	'''
		
	#vision algorithms to detect the board
	board = board_vision.detectBoard(img)

	if(board == None):
		print('board could not be detected')
		return
	
	#if first board, don't do anything for accuracy
	if(lastBoard == None):
		lastBoard = board
		print('board moved, not computing')
		return

	#print board.outline
	#print lastBoard.outline
 
	#only use board if it is in the same location for 2 frames to eliminate
	#instability
	if(np.array_equal(lastBoard.outline, board.outline) != True):
		lastBoard = board
		print('board moved, not computing')
		return

	#only use a board if it is the same state for 2 frames to eliminate instability
	if(np.array_equal(lastBoard.boardState, board.boardState) != True):
		print('last board state changed, wait one frame')
		lastBoard = board
		return

	lastBoard = board

	centers = []	
	for cluster in board.squareCenters:
		centers.append(cluster.center)
	
	x,y,z = getWorldCoordinates(centers, data.xyz, data.width)
	
	result = TicTacToe()
	result.header = data.header
	result.x = x
	result.y = y
	result.z = z
	result.state = board.boardState
	
	#publish the board state as well as the real world xyz coordinates to the AI
	publisher.publish(result)
	
	
	

def listener():
	rospy.init_node('board_finder')
	global publisher
	publisher = rospy.Publisher('board_finder/TicTacToe', TicTacToe, queue_size=1)
	rospy.Subscriber("board_finder/Kinect_Image", Kinect_Image, callback)
	print("Starting listener")
	
	rospy.Rate(2)
	rospy.spin()
	
if __name__ == '__main__':
	print "started finder"
	listener()
	
	
