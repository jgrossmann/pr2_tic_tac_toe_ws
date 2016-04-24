#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
import board_vision

def getWorldCoordinates(centers, coordinates):
	pass
	#match the pixel values with the indexes in coordinates
	#to get the world coordinates of each square center

def callback(data):
	print('callback')
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
		
	centers, state = board_vision.detectBoard(img)
	
	if(centers == None || state == None):
		print('board could not be detected')
		return
	
	centers = getWorldCoordinates(centers, data.xyz)
	
	#publish(message)
	
	

def listener():
	rospy.init_node('board_finder')
	rospy.Subscriber("/kinect_image", msg, callback)
	print("Starting listener")
	rospy.spin()
	
if __name__ == '__main__':
	listener()
	
	
