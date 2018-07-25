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
        
	
	
	
	






