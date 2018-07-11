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
        self.x = 0
        self.SPEED = 1.5 	#[rad/s]
        self._speed = 0		#temp speed
        self.odometry = Odometry()

        ############################### SUBSCRIBERS #####################################
        rospy.Subscriber("speedMotors_float", Float32MultiArray, self.speed_f)
        rospy.Subscriber("robotPosition", Float32MultiArray, self.robotPosition_cb)
        rospy.Subscriber("uControl", Float32MultiArray, self.uControl_cb)
        rospy.Subscriber("cmd_vel", Twist, self.cmd_vel_cb)

        ###********** INIT NODE **********###
        r = rospy.Rate(10)              #10Hz
        print "Node initialized 10hz"

        ###******** SETTING ARRAYS *******###

        self.setpoint = Float32MultiArray()
        self.setpoint.layout.dim.append(MultiArrayDimension())
        self.setpoint.layout.dim[0].label = "height"
        self.setpoint.layout.dim[0].size = 2
        self.setpoint.layout.dim[0].stride = 1
        self.setpoint.layout.data_offset = 0
        self.setpoint.data = [0]*2

        ###********** INIT ARRAYS ********###

        self.setpoint.data[0]= 5.4
        self.setpoint.data[1]= 6.8

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
        ##TODO: calcular la velocidad de las ruedas apartir de la velocidad del robot
        print(data)
    
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
        
	
	
	
	






