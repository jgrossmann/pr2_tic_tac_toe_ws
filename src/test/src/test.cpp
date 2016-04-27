#include <ros/ros.h>
#include <tf/transform_listener.h>


using namespace std;

//ros::Publisher publisher;

//string linkid("base_link");




int main(int argc, char** argv) {

	ros::init(argc, argv, "point_cloud_convertor");
	ROS_INFO("ros init done");
	ros::NodeHandle nh;
	/*
	ros::Subscriber sub = nh.subscribe(
						"/head_mount_kinect/depth_registered/points",
						2,
						callback);
	publisher = nh.advertise<board_finder::Kinect_Image>("board_finder/Kinect_Image", 1);
 	ros::Rate loop_rate(2);*/
	tf::TransformListener listener;
	if(nh.ok()) {
		try {
			tf::StampedTransform transform;


			listener.lookupTransform("base_link", "random", ros::Time(0),
	 transform);
		}catch (tf::TransformException ex){
			
		}
	}

	ros::spin();
}
