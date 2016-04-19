#include <moveit/move_group_interface/move_group.h>
#include <iostream>
#include "move_arm.cpp" 

//we need async spinner to do tasks one after another 
int main(int argc, char **argv)
{

  ros::init(argc, argv, "move_arm_example");
  ros::NodeHandle node_handle;

  int a = move_arm(.30, .11, 1, 1,'l'); //write instructions to left arm

  int b = move_arm(.30, -.5, 1, 1,'r'); //write instructions to left arm

  std::cout << a << std::endl;
  return 0;
}
