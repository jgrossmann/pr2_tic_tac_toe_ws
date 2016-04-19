#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
import sys
from actionlib_msgs.msg import *
import actionlib
from pr2_controllers_msgs.msg import *


client = actionlib.SimpleActionClient("/head_traj_controller/point_head_action",
								PointHeadAction)

def moveHead(frame_id, x, y, z):
	g = PointHeadGoal()
	g.target.header.frame_id = frame_id
	g.target.point.x = x
	g.target.point.y = y
	g.target.point.z = z
	g.min_duration = rospy.Duration(0.5)
	
    client.send_goal(g)
	client.wait_for_result()
	
	if client.get_state() == GoalStatus.SUCCEEDED:
		print "Succeeded"
	else:
		print "Failed"


	
def findBoard(req):
	client.wait_for_server()
	#msg = rospy.wait_for_message("/kinect_image/xyz_and_rgb", MsgType)
	#perform image processing
	#if result is no board, moveHead(frame_id, x, y, z)
	#if result is board found, return true.
	#if get to end without finding board, return False.
	pass
	



