#include <moveit/move_group_interface/move_group.h>
#include <iostream>
 
void move_arm(double x, double y, double z, double w, char arm)
{
  if (arm == 'l') {
  moveit::planning_interface::MoveGroup l_arm_move_group("left_arm");
  geometry_msgs::Pose goal_end_effector_pose;
  goal_end_effector_pose.orientation.w = w; //1, .28, .7, 1
  goal_end_effector_pose.position.x = x;
  goal_end_effector_pose.position.y = y;
  goal_end_effector_pose.position.z = z;
  //l_arm_move_group.setRandomTarget();  

  l_arm_move_group.setPoseTarget(goal_end_effector_pose);

  // plan the motion and then move the group to the sampled target 
  l_arm_move_group.asyncMove();

  sleep(3.0);
  l_arm_move_group.stop();
  sleep(2.0);
  }

  else if (arm == 'r') {
  moveit::planning_interface::MoveGroup r_arm_move_group("right_arm");
  geometry_msgs::Pose goal_end_effector_pose;
  goal_end_effector_pose.orientation.w = w; //1, .28, .7, 1
  goal_end_effector_pose.position.x = x;
  goal_end_effector_pose.position.y = y;
  goal_end_effector_pose.position.z = z;
  //l_arm_move_group.setRandomTarget();  
  r_arm_move_group.setPoseTarget(goal_end_effector_pose);
  // plan the motion and then move the group to the sampled target 
  r_arm_move_group.asyncMove();
  }

 
	
}
