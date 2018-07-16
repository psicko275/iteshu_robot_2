#!/usr/bin/env python

import os
import fcntl
import rospy

from std_msgs.msg import UInt16MultiArray
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayDimension
from std_msgs.msg import String
from std_msgs.msg import Int16
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class IteshuRobot():
    def __init__(self):
        self.R=0.052   #Wheel radius [m]
        self.L=0.264   #Distance between the wheels [m]
        

class IteshuDriver():
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        ###******* INIT PUBLISHERS *******###
        print "Setting publisher..."
        ##	pub = rospy.Publisher('setPoint', UInt16MultiArray, queue_size=1)
        self.pub_f = rospy.Publisher('setPoint_f', Float32MultiArray, queue_size=1)
        self.pub_odom = rospy.Publisher('odom', Odometry, queue_size=1)
        print "Publishers ok"
        print "Starting Node..."
        
        ############################### SUBSCRIBERS #####################################
        rospy.Subscriber("speedMotors_float", Float32MultiArray, self.speed_f)
        rospy.Subscriber("robotPosition", Float32MultiArray, self.robotPosition_cb)
        rospy.Subscriber("uControl", Float32MultiArray, self.uControl_cb)
        rospy.Subscriber("cmd_vel", Twist, self.cmd_vel_cb)

        ############ CONSTANTS ################
        self.x = 0
        self.SPEED = 1.5 	#[rad/s]
        self._speed = 0		#temp speed
        self.wl=0 #right wheel speed [rad/sec]
        self.wr=0 #right wheel speed [rad/sec]
        self.odometry = Odometry()
        self.robot=IteshuRobot()
        self.setpoint = Float32MultiArray() ##Array that contains the wheel speeds [lef][right]
       
        ###******** SETTING ARRAYS *******###
        self.setpoint.layout.dim.append(MultiArrayDimension())
        self.setpoint.layout.dim[0].label = "height"
        self.setpoint.layout.dim[0].size = 2
        self.setpoint.layout.dim[0].stride = 1
        self.setpoint.layout.data_offset = 0
        self.setpoint.data = [0]*2

        ###********** INIT ARRAYS ********###
        self.setpoint.data[0]= 0
        self.setpoint.data[1]= 0
        
        ###********** INIT NODE **********###
        r = rospy.Rate(10)              #10Hz
        print "Node initialized 10hz"
        print(self.setpoint.data[0])
        print(self.setpoint.data[1])
        while not rospy.is_shutdown():
            self.pub_odom.publish(self.odometry)
            r.sleep()

    def speed_f(self, data):
	    print(str(data.data[0])+"\t"+str(data.data[1])+"\t"+str(data.data[2])+"\n")
	    #file1.write(str(data.data[0])+"\t"+str(data.data[1])+"\t"+str(data.data[2])+"\n")
        
	
    def robotPosition_cb(self, data):
    	print(str(data.data[0])+"\t"+str(data.data[1])+"\t"+str(data.data[2])+"\n")
	    #file2.write(str(data.data[0])+"\t"+str(data.data[1])+"\t"+str(data.data[2])+"\n")

    def uControl_cb(self, data):
    	print(str(data.data[0])+"\t"+str(data.data[1])+"\t"+str(data.data[2])+"\n")
	    #file3.write(str(data.data[0])+"\t"+str(data.data[1])+"\t"+str(data.data[2])+"\n")

    def cmd_vel_cb(self, data):
        ## This function computes the wheel speed from the robot's speed
        ##      2v-Lw        2v+Lw
        ## wl = -----;  wr = ------
        ##        2R           2R
        v= data.linear.x
        w= data.angular.z
        self.wl=(2*v-self.robot.L*w)/(2*self.robot.R) #right wheel speed (rad/sec)
        self.wr=(2*v+self.robot.L*w)/(2*self.robot.R) #right wheel speed (rad/sec)
        print "wl= ", self.wl
        print "wl= ", self.wr
        self.setpoint.data[0]= self.wr
        self.setpoint.data[1]= self.wl
        self.pub_f.publish(self.setpoint)
        
    
    def cleanup(self):
        #Stop the robot before aborting the node	
	    self.setpoint.data[0]= 0
	    self.setpoint.data[1]= 0
	    self.pub_f.publish(self.setpoint)
        


############################### MAIN PROGRAM ####################################
if __name__ == "__main__":
    rospy.init_node("iteshu_driver_translator", anonymous=True)
    try:
	    IteshuDriver()
    except:
        rospy.logfatal("iteshu_driver_translator died")
        
	
	
	
	






