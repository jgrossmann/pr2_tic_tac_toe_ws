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

publisher = None
lastBoard = None

def getWorldCoordinates(centers, coordinates):
	worldCoordinates = []
	for center in centers:
		index = center.x * center.y * 3
		worldCoordinates.append([coordinates[index], coordinates[index+1], coordinates[index+2]])
		
	return worldCoordinates

def callback(data):
	print('callback')
	global lastBoard

	print(rospy.get_caller_id() + " "+ str(data.header.stamp))
	bridge = CvBridge()
	
	try:
		img = bridge.imgmsg_to_cv2(data.rgb, "rgb8")
		
	except CvBridgeError as e:
		print(e)
		
	
	try:
		cv2.imwrite('image.jpg', img)
	except:
		print("Error writing image")
		
	board = board_vision.detectBoard(img)

	if(board == None):
		print('board could not be detected')
		return

	if(lastBoard == None):
		lastBoard = board
		print('board moved, not computing')
		return

	if(lastBoard.outline != board.outline):
		lastBoard = board
		print('board moved, not computing')
		return

	lastBoard = board

	centers = []	
	for cluster in board.squareCenters:
		centers.append(cluster.center)
	
	print board.state
	centers = getWorldCoordinates(centers, data.xyz)
	
	result = TicTacToe()
	result.header = data.header
	result.centers = centers
	result.state = board.state
	
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
	listener()
	
	
