#include <ros/ros.h>
#include <pcl_ros/point_cloud.h>
#include <pcl/point_types.h>
#include <boost/foreach.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <sstream>
#include "board_finder/Kinect_Image.h"
#include <cv_bridge/cv_bridge.h>
#include <image_transport/image_transport.h>
#include <sensor_msgs/Image.h>
#include <tf/transform_listener.h>
#include <pcl_ros/impl/transforms.hpp>
#include <pcl_ros/transforms.h>
#include <pcl_conversions/pcl_conversions.h>
#include <sensor_msgs/PointCloud2.h>

using namespace std;

tf::TransformListener *listener; //finds transform between reference states
ros::Publisher publisher;	     //publishes transformed kinect images to vision
string linkid("odom_combined");	 //name of reference frame to use


//receives kinect depth_registered points from connect
void callback(const sensor_msgs::PointCloud2::ConstPtr& msg) {
	sensor_msgs::PointCloud2 tmsg;

	ostringstream width;
	width << msg->width;
	//ROS_INFO(width.str().c_str());

	ostringstream height;
	height << msg->height;
	//ROS_INFO(height.str().c_str());

	//std::cout << msg->header.frame_id << std::endl;
	//std::cout << msg->header.stamp << std::endl;

	tf::StampedTransform transform;


	//ROS_INFO("looking up transform");
	
	//transform the kinect image to odom_combined reference frame
	try {
		listener->waitForTransform(linkid, msg->header.frame_id,
                              msg->header.stamp, ros::Duration(0.25));
		listener->lookupTransform(linkid, msg->header.frame_id, msg->header.stamp, transform);
		//ROS_INFO("looked up transform");
		pcl_ros::transformPointCloud(linkid, *msg, tmsg, *listener);
	}catch(tf::TransformException ex) {
		//ROS_INFO("exception");
		//std::cerr << ex.what();
		return;
	}
	//ROS_INFO("transformed coordinates");


	pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZRGB>);
	pcl::fromROSMsg (tmsg, *cloud);

	//must set the height and width of pointcloud to use pcl
	cloud->width = 640;
	cloud->height = 480;
	cloud->points.resize(cloud->width * cloud->height * 3);

	 //std::cout << tmsg.header.frame_id << std::endl;

	//xyz array to send to vision
	std::vector<float> xyz(cloud->width * cloud->height * 3);

	//separate the RGB image from XYZ coordinates
	//set the xyz coordinates into their own array
	cv::Mat imageFrame;
	if (cloud->isOrganized())
	{
		ROS_INFO("is organized");
		imageFrame = cv::Mat(cloud->height, cloud->width, CV_8UC3); 
		{

			int index;
	
			for (int h=0; h<imageFrame.rows; h++) 
			{
				for (int w=0; w<imageFrame.cols; w++) 
				{
				    pcl::PointXYZRGB point = cloud->at(w, h);
			
					index = h * (cloud->width * 3) + (w * 3);

					if(w == 421 && h == 373) {
						std::cout << point.x << std::endl;
					}
					if(h == 421 && w == 373) {
						std::cout << point.x << std::endl;
					}
				
					xyz[index] = point.x;
					xyz[index+1] = point.y;
					xyz[index+2] = point.z;	
				
				    Eigen::Vector3i rgb = point.getRGBVector3i();

				    imageFrame.at<cv::Vec3b>(h,w)[0] = rgb[2];
				    imageFrame.at<cv::Vec3b>(h,w)[1] = rgb[1];
				    imageFrame.at<cv::Vec3b>(h,w)[2] = rgb[0];
				}
			}
		}
	}

	cv_bridge::CvImage bridge = cv_bridge::CvImage(tmsg.header, "rgb8", imageFrame);
	sensor_msgs::ImagePtr outputImage = bridge.toImageMsg();

	board_finder::Kinect_Image newMessage;
	newMessage.header = tmsg.header;
	newMessage.rgb = *outputImage;
	newMessage.width = cloud->width;
	newMessage.height = cloud->height;

	newMessage.xyz = xyz;

	//publish transformed and separated image and xyz to vision
	publisher.publish(newMessage);


	/*
	TESTING
	vector<int> compression_params;
	compression_params.push_back(CV_IMWRITE_PNG_COMPRESSION);
	compression_params.push_back(9);

	cv::imwrite("kinect_image.png", imageFrame, compression_params);
	ROS_INFO("wrote image");

	//send message on publisher
	//have to create a message type first
	*/
}


int main(int argc, char** argv) {

	ros::init(argc, argv, "point_cloud_convertor");
	ROS_INFO("ros init done");
	ros::NodeHandle nh;
	listener = new (tf::TransformListener);

	publisher = nh.advertise<board_finder::Kinect_Image>("board_finder/Kinect_Image", 2);
 	ros::Rate loop_rate(2);

	ros::Subscriber sub = nh.subscribe(
						"/head_mount_kinect/depth_registered/points",
						2,
						callback);
	

	ros::spin();
}
