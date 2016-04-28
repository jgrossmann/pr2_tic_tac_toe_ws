#include "move_arm.cpp"
#include <stdlib.h>
#include <string>
#include <sstream>
#include "board_finder/TicTacToe.h"

//There is a known bug with the to_string function, this patch solves it
//http://stackoverflow.com/questions/12975341/to-string-is-not-a-member-of-std-says-so-g
namespace patch
{
    template < typename T > std::string to_string( const T& n )
    {
        std::ostringstream stm ;
        stm << n ;
        return stm.str() ;
    }
}

//Global counter variable useful for disambiguating model names
int ctr = 0;

//Global path to models
std::string path_to_models = "/home/cs4167/tmp/test/pr2_example_ws-master/src/system_launch/models/";

//Position of the board, the vision algorithm modifies this based on its sensing
int gameBoard [9] = {0, 0, 0, 0, 0, 0, 0, 0, 0};

//Centers of the gameboard stored here
double squareCenters [9][3] = {0};

bool robotTurn = false;



//Human spawns a model
void B(int piece, double x, double y, double z) {

//spawn the model
  std::string model;
  if (piece == 1)
	std::string model = "coke_can.urdf";//"X.urdf"; //Change this in the final code
  else
	std::string model = "coke_can.urdf";//"O.urdf"; //Change this in the final code
  std::string name = patch::to_string(ctr);
  std::string coords = " -x " + patch::to_string(x) +  " -y " + patch::to_string(y) + " -z " + patch::to_string(z);
  std::string command = "rosrun gazebo_ros spawn_model -file " + path_to_models + model + " -urdf -model " + name + coords;
  system(command.c_str());
  ctr += 1;
}



//Given input from the AI, execute the move and model spawning
//piece 1 is X, 2 is O, 0 is nothing
void A(int piece, double x, double y, double z) {
  //Move the right arm to the board
  z = z+.1; //to avoid collisions, elevate the gripper from the board
  move_arm(x, y, z, 1,'r');  //Todo: orientation of the gripper, w, hasn't been played with

  //spawn the model
  B(piece,x,y,z);

  //Move the arm back to a graceful position
  move_arm(.3, .5, 1, 1,'r');
  return;
}


//Use our vision algorithm to sense the board, get square centers and game state
void C() {

//modify squareCenters, which is a 9 by 3 array of doubles containing centers of the board.

//modify gameBoard variable

}

void visionCallback(const board_finder::TicTacToe::ConstPtr &msg) {


	for(int i=0; i < 9; i++) {
		squareCenters[i][0] = msg->x[i];
		squareCenters[i][1] = msg->y[i];
		squareCenters[i][2] = msg->z[i];

		gameBoard[i] = msg->state[i];
	}

	//gameBoard = msg->state;

	ROS_INFO("updated board state");
	
}


void moveArmsToDefaultPose() {
	move_arm(.30, .5, 1, 1,'l');
	ros::Duration(1).sleep();
	move_arm(.30, -.5, 1, 1, 'r');
}



int main(int argc, char **argv)
{
  ros::init(argc, argv, "move_arm_example");
  ros::NodeHandle node_handle;

  moveArmsToDefaultPose();
  //Get left arm out of the way
  //move_arm(.30, .5, 1, 1,'l'); //write instructions to left arm

  ros::Subscriber sub = node_handle.subscribe(
						"board_finder/TicTacToe",
						2,
						visionCallback);

  ros::spin();

  //Start the Python game, queries who goes first

  //1: feed input to robot (skip if human goes first)

  //2: Accept human's move, and spawn the model

  //3: Let vision parse the image

  //4: send updated game state to the AI, indicating the human's move, and receive the robot's move

  //5: If game is over, indicate so (if robot won, execute the robot movement), the exit this while loop

  //6. If game is not over, go back to 1. 


  std::cout << "made it to the end" << std::endl;
  return 1;
}




//Test code, unused:

  //establish a default pose for the right arm that it will return to
  //move_arm(.3, .5, 1, 1,'r'); //write instructions to right arm



  //b = move_arm(.28, -.7, 1, 1,'r'); //write instructions to left arm
  //b = move_arm(.26, -.7, 1, 1,'r'); //write instructions to left arm
  //b = move_arm(.24, -.7, 1, 1,'r'); //write instructions to left arm
  //b = move_arm(.22, -.7, 1, 1,'r'); //write instructions to left arm
  //b = move_arm(.20, -.7, 1, 1,'r'); //write instructions to left arm
  //int a = move_arm(.3, 1, 1, 1,'l'); //write instructions to right arm

  //spawn model
 // system("rosrun gazebo_ros spawn_model -file /home/cs4167/tmp/test/pr2_example_ws-master/src/system_launch/models/coke_can.urdf -urdf -model coke_can3 -y 0.2 -x 1.5");
  //a = move_arm(.30, .7, 1, 1,'l'); //write instructions to left arm

//move_arm_main.cpp
//Displaying move_arm_main.cpp.
