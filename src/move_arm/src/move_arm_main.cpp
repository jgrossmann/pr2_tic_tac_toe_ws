#include <moveit/move_group_interface/move_group.h>
#include <iostream>
#include "move_arm.cpp" 


int main(int argc, char **argv)
{

  ros::init(argc, argv, "move_arm_example");
  //ros::NodeHandle node_handle;

  //int a = move_arm(.30, .5, 1, 1,'l'); //write instructions to left arm
  move_arm(.30, .5, 1, 1,'l'); //write instructions to left arm
  //move_arm(.63, .088, .7, 1.55, 'l');
  //int b = move_arm(.30, -.5, 1, 1,'r'); //write instructions to left arm
  move_arm(.30, -.5, 1, 1,'r'); //write instructions to left arm
  //move_arm(.549, -.182, 1, 1, 'r');

  //std::cout << a << std::endl;
  std::cout << "done" << std::endl;
  return 0;
}
