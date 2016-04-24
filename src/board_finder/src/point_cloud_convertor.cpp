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

using namespace std;

ros::Publisher publisher;



void callback(const sensor_msgs::PointCloud2::ConstPtr& msg) {
    ostringstream width;
	width << msg->width;
    ROS_INFO(width.str().c_str());

    ostringstream height;
	height << msg->height;
    ROS_INFO(height.str().c_str());

	pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZRGB>);
	pcl::fromROSMsg (*msg, *cloud);
	
    cloud->width = 640;
	cloud->height = 480;
	cloud->points.resize(cloud->width * cloud->height);

    
    
	cv::Mat imageFrame;
	if (cloud->isOrganized())
	{
        ROS_INFO("is organized");
		imageFrame = cv::Mat(cloud->height, cloud->width, CV_8UC3); 
		{

		    for (int h=0; h<imageFrame.rows; h++) 
		    {
		        for (int w=0; w<imageFrame.cols; w++) 
		        {
		            pcl::PointXYZRGB point = cloud->at(w, h);

		            Eigen::Vector3i rgb = point.getRGBVector3i();

		            imageFrame.at<cv::Vec3b>(h,w)[0] = rgb[2];
		            imageFrame.at<cv::Vec3b>(h,w)[1] = rgb[1];
		            imageFrame.at<cv::Vec3b>(h,w)[2] = rgb[0];
		        }
		    }
		}
	}
	
	cv_bridge::CvImage bridge = cv_bridge::CvImage(msg->header, "rgb8", imageFrame);
	sensor_msgs::ImagePtr outputImage = bridge.toImageMsg();

	board_finder::Kinect_Image newMessage;
	newMessage.header = msg->header;
	newMessage.rgb = *outputImage;
	newMessage.width = cloud->width;
	newMessage.height = cloud->height;
	
	
	publisher.publish(newMessage);

    vector<int> compression_params;
    compression_params.push_back(CV_IMWRITE_PNG_COMPRESSION);
    compression_params.push_back(9);

	cv::imwrite("kinect_image.png", imageFrame, compression_params);
	ROS_INFO("wrote image");

	//send message on publisher
	//have to create a message type first
}

int main(int argc, char** argv) {

	ros::init(argc, argv, "point_cloud_convertor");
	ros::NodeHandle nh;
	ros::Subscriber sub = nh.subscribe(
						"/head_mount_kinect/depth_registered/points",
						2,
						callback);
	publisher = nh.advertise<board_finder::Kinect_Image>("board_finder/Kinect_Image", 1);
 	ros::Rate loop_rate(2);

	ros::spin();
}
