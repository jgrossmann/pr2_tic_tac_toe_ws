Tic Tac Toe Pr2

Authors:
John Grossmann
Vaibhav Vavilala

Link to video: https://www.youtube.com/watch?v=giZJETH3FaA

This software was tested with ROS Indigo.

To use, source /opt/ros/indigo/setup.bash or wherever the ros indigo setup.bash
file is located.

Run catkin_make in the pr2_tic_tac_toe_ws base directory.

Make sure that the Kinect is setup for the Pr2 robot in gazebo. We had to 
type export KINECT1=true to enable it to work.

After the make is done, source the setup by typing source devel/setup.bash in the pr2_tic_tac_toe_ws base directory. This must be done in every terminal you use.


In one terminal, type 'roslaunch system_launch tic_tac_toe_gazebo.launch'. This launches Gazebo with the appropriate conditions and models.

Wait until Gazebo is fully loaded. Then, in another terminal, type: 'roslaunch system_launch tic_tac_toe_vision.launch'. This Moves the head of the Pr2 down, and starts the vision node of the pr2. 

Start another terminal and type: 'rosrun board_finder TTT.py' to start the AI for the robot. In this terminal, wait for a prompt to start the game. This terminal will also prompt you for your choice of board space to place each move. 

The board spaces are labeled 1 to 9. From the robot's point of view, 1 is the top left space, 2 is the top center space, 3 is the top right space, 4 is the space below 1, and 9 is the bottom right space.




