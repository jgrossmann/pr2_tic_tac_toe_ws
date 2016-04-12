#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from sensor_msgs.msg import PointCloud2
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError


def callback(data):
	print('callback')
	print(rospy.get_caller_id() + " "+ str(data.header.stamp))
	
	bridge = CvBridge()
	
	rgb = np.arange((len(data.data)/32)*3, dtype=np.uint8)

	index = 0
	for i in xrange(16, (len(data.data)/32)*3, 32):
		rgb[index] = data.data[i]
		index += 1
		rgb[index] = data.data[i+1]
		index += 1
		rgb[index] = data.data[i+2]
		index += 1

	print rgb

	try:
		pass
		#img = bridge.imgmsg_to_cv2(rgb, "rgb8")
	except CvBridgeError as e:
		print(e)
		
	
	try:
		pass
		#cv2.imwrite('image.jpg', img)
	except:
		print("Error writing image")
		

	
	

def listener():
	rospy.init_node('camera_listener', anonymous=True)
	#rospy.Subscriber("/wide_stereo/left/image_color", Image, callback)
	rospy.Subscriber("/head_mount_kinect/depth_registered/points", PointCloud2, callback)
	print("Starting listener")
	rospy.spin()
	
if __name__ == '__main__':
	listener()
