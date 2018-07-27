#!/usr/bin/env python

import os
import fcntl
import sys, select, termios, tty
import rospy
import math
import time

from os.path import expanduser

import shutil
import paramiko

from std_msgs.msg import UInt16MultiArray
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayDimension
from std_msgs.msg import String
from std_msgs.msg import Int16

global file1, file2, file3
file1 = None
file2 = None
file3 = None

########## Real robot variables ############
t = 0
x = 0
y = 0
theta = 0
wr = 0
wl = 0

############################### SUBSCRIBERS #####################################
#def callback(data):
#    print(data.data)

def speed_f(data):
#	print(str(data.data[0])+"\t"+str(data.data[1])+"\t"+str(data.data[2])+"\n")
	global file1
	file1.write(str(data.data[0])+"\t"+str(data.data[1])+"\t"+str(data.data[2])+"\n")
	
	global t, wr, wl			#setting a globals variables
	t = float(data.data[0])
	wr = float(data.data[1])
	wl = float(data.data[2])
	
def robotPosition_cb(data):
#	print(str(data.data[0])+"\t"+str(data.data[1])+"\t"+str(data.data[2])+"\n")
	global file2
	file2.write(str(data.data[0])+"\t"+str(data.data[1])+"\t"+str(data.data[2])+"\n")
	
	global theta, x, y
	theta = float(data.data[0])
	x = data.data[1]
	y = float(data.data[2])
	
def uControl_cb(data):
#	print(str(data.data[0])+"\t"+str(data.data[1])+"\t"+str(data.data[2])+"\n")
	global file3
	file3.write(str(data.data[0])+"\t"+str(data.data[1])+"\t"+str(data.data[2])+"\n")
	
def listener():
    #rospy.init_node('listener', anonymous=True)

#	rospy.Subscriber("adc", Int16, callback)
	rospy.Subscriber("speedMotors_float", Float32MultiArray, speed_f)
	rospy.Subscriber("robotPosition", Float32MultiArray, robotPosition_cb)
	rospy.Subscriber("uControl", Float32MultiArray, uControl_cb)
#    rospy.spin()

############################### MAIN PROGRAM ####################################
if __name__ == "__main__":

    home = expanduser("~")
    file1 = open(home+"/Documentos/data/robotWheelSpeed.txt","w")
    file2 = open(home+"/Documentos/data/robotPosition.txt","w")
    file3 = open(home+"/Documentos/data/uControl.txt","w")

    listener();

    ###********** INIT NODE **********###
    rospy.init_node('saveData', anonymous=True)
    r = rospy.Rate(10)              #10Hz
    print "Node initialized 10hz"

    ####while#####
    while not rospy.is_shutdown():
#        print "hola"
        r.sleep()
    #########	

    #Stop program
    rospy.signal_shutdown("kill app before close files")
    file1.close()
    file2.close()
    file3.close()

    #file1 = open("/home/robot/Documentos/data/robotWheelSpeed.txt","w")
    #file2 = open("/home/robot/Documentos/data/robotPosition.txt","w")
    #file3 = open("/home/robot/Documentos/data/uControl.txt","w")
    #shutil.copyfile("/home/robot/Documentos/data/robotWheelSpeed.txt","/media/robot/2789-3D1F/data/robotWheelSpeed.txt")
    #shutil.copyfile("/home/robot/Documentos/data/robotPosition.txt","/media/robot/2789-3D1F/data/robotPosition.txt")
    #shutil.copyfile("/home/robot/Documentos/data/uControl.txt","/media/robot/2789-3D1F/data/uControl.txt")

    ############## send data to local pc (lenovo remote)	
    #ssh = paramiko.SSHClient() 
    #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect('192.168.5.4', 22, 'josemiguel', 'iteshu')
    #sftp = ssh.open_sftp()
    #sftp.put("/home/robot/Escritorio/h.txt", "/home/josemiguel/Escritorio/h.txt")
    #sftp.close()
    #ssh.close()
    ################## end send data files #################

    print "closed app"

