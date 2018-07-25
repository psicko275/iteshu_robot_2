#!/usr/bin/env python

import os
import fcntl
import rospy


from sensor_msgs.msg import LaserScan

    

class LaserFilter():
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        ###******* INIT PUBLISHERS *******###
        self.scan_filtered_pub = rospy.Publisher('base_scan', LaserScan, queue_size=1)


        ############################### SUBSCRIBERS #####################################
        rospy.Subscriber("scan", LaserScan, self.scan_cb)


        ############ CONSTANTS ################
        self.scan_msg = LaserScan()
        self.max_limit= 5


        ###********** INIT NODE **********###
        r = rospy.Rate(10)              #10Hz
        print "Node initialized 10hz"
        while not rospy.is_shutdown():
            self.scan_filtered_pub.publish(self.scan_msg)
            r.sleep()

    def scan_cb(self, msg):
        self.scan_msg = LaserScan()
        self.scan_msg.header = msg.header
        self.scan_msg.angle_min = msg.angle_min
        self.scan_msg.angle_max = msg.angle_max
        self.scan_msg.angle_increment = msg.angle_increment
        self.scan_msg.time_increment = msg.time_increment
        self.scan_msg.scan_time = msg.scan_time
        self.scan_msg.range_min = msg.range_min
        self.scan_msg.range_max = msg.range_max
        for element in msg.ranges:
            if element == float('Inf'):
                self.scan_msg.ranges.append(self.max_limit)
            else:
                self.scan_msg.ranges.append(element) 

        
	
  
        
    
    def cleanup(self):
        #Stop the robot before aborting the node	
	    print "clean up is doing nothing"
        


############################### MAIN PROGRAM ####################################
if __name__ == "__main__":
    rospy.init_node("laser_filter", anonymous=True)
    try:
	    LaserFilter()
    except:
        rospy.logfatal("laser_filter died")
        
	
	
	
	






