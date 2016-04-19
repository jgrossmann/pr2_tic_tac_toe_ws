#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
import board_vision_lib

done = False

def callback(data):
	print('callback')
	print(rospy.get_caller_id() + " "+ str(data.header.stamp))
	bridge = CvBridge()
	
	try:
		img = bridge.imgmsg_to_cv2(data, "bgr8")
	except CvBridgeError as e:
		print(e)
		
	
	try:
		cv2.imwrite('image.jpg', img)
	except:
		print("Error writing image")
		
	done = True
	
	

def listener():
	rospy.init_node('camera_listener', anonymous=True)
	rospy.Subscriber("/wide_stereo/left/image_color", Image, callback)
	print("Starting listener")
	rospy.spin()
	
if __name__ == '__main__':
	listener()
