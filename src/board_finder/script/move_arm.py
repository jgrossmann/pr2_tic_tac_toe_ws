#!/usr/bin/env python
import moveit_commander
import numpy as np
import rospy
import math


def move_arm(x, y, z, w, arm):
	#insert code to move arm
	pass

if __name__ == '__main__':
	rospy.init_node("moveit_demo_node")

	#get the robot
	robot  = moveit_commander.RobotCommander()

	#lets plan some trajectories for the left arm
	group = robot.get_group('left_arm')

	jointValues = group.get_current_joint_values()
	print jointValues
	print group.get_active_joints()
	
	jointValues[5] = -math.pi/4.0
	group.set_joint_value_target(jointValues)

	print jointValues
	plan = group.plan()

	#generate a random pose for the end effector
	#pose = group.get_random_pose()

	#generate a trajectory to get the gripper from
	#its current location to this new pose
	#trajectory = group.plan(pose)

'''
print (
import moveit_commander
import numpy as np
import rospy

#initial a ros node
rospy.init_node("moveit_demo_node")

#get the robot
robot  = moveit_commander.RobotCommander()

#lets plan some trajectories for the left arm
group = robot.get_group('left_arm')

#generate a random pose for the end effector
pose = group.get_random_pose()

#generate a trajectory to get the gripper from
#its current location to this new pose
trajectory = group.plan(pose)
    )

#import IPython
#IPython.embed()
#group.execute(trajectory)
'''
