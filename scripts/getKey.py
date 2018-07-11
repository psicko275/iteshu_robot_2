#!/usr/bin/env python

import os
import fcntl
import sys, select, termios, tty
import rospy

from std_msgs.msg import UInt16MultiArray
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayDimension
from std_msgs.msg import String
from std_msgs.msg import Int16

x = 0
SPEED = 1.5 	#[rad/s]
_speed = 0;		#temp speed

############################## GET KEY ADVANCED #################################
def getch():
  fd = sys.stdin.fileno()

  oldterm = termios.tcgetattr(fd)
  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)

  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

  try:        
    while 1:            
      try:
        c = sys.stdin.read(1)
        break
      except IOError: pass
  finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
  return c

############################### GET BASIC KEY ###################################
def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

############################### SUBSCRIBERS #####################################
#def callback(data):
#    print(data.data)

def speed_f(data):
#	print(str(data.data[0])+"\t"+str(data.data[1])+"\t"+str(data.data[2])+"\n")
	file1.write(str(data.data[0])+"\t"+str(data.data[1])+"\t"+str(data.data[2])+"\n")
	
def robotPosition_cb(data):
#	print(str(data.data[0])+"\t"+str(data.data[1])+"\t"+str(data.data[2])+"\n")
	file2.write(str(data.data[0])+"\t"+str(data.data[1])+"\t"+str(data.data[2])+"\n")

def uControl_cb(data):
#	print(str(data.data[0])+"\t"+str(data.data[1])+"\t"+str(data.data[2])+"\n")
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

	file1 = open("/home/beny/Dropbox/iteshu_robot/Hector/data/robotWheelSpeed.txt","w")
	file2 = open("/home/beny/Dropbox/iteshu_robot/Hector/data/robotPosition.txt","w")
	file3 = open("/home/beny/Dropbox/iteshu_robot/Hector/data/uControl.txt","w")
	
	settings = termios.tcgetattr(sys.stdin)
	
	listener();
	
	###******* INIT PUBLISHERS *******###
	print "Setting publisher..."
##	pub = rospy.Publisher('setPoint', UInt16MultiArray, queue_size=1)
	pub_f = rospy.Publisher('setPoint_f', Float32MultiArray, queue_size=1)
	print "Publisher ok"
	print "Starting Node..."
	
	###********** INIT NODE **********###
	rospy.init_node('publisher', anonymous=True)
	r = rospy.Rate(10)              #10Hz
	print "Node initialized 10hz"
	
	###******** SETTING ARRAYS *******###
	m = UInt16MultiArray()
	m.layout.dim.append(MultiArrayDimension())
	m.layout.dim[0].label = "height"
	m.layout.dim[0].size = 2
	m.layout.dim[0].stride = 1
	m.layout.data_offset = 0
	m.data = [0]*2
	
	setpoint = Float32MultiArray()
	setpoint.layout.dim.append(MultiArrayDimension())
	setpoint.layout.dim[0].label = "height"
	setpoint.layout.dim[0].size = 2
	setpoint.layout.dim[0].stride = 1
	setpoint.layout.data_offset = 0
	setpoint.data = [0]*2
	
	###********** INIT ARRAYS ********###
	m.data[0]= 0;
	m.data[1]= 0;
	
	setpoint.data[0]= 5.4;
	setpoint.data[1]= 6.8;
	
	print(setpoint.data[0])
	print(setpoint.data[1])
	
	##***************** Move action ******************##
	##****** i = Move ----- j = Left ----- l = Right *##
	##****** a = Front ---- s = Stop ----- d = Back **##
	##****** TO CANCEL EXECUTION PRESS BLANKSPACE ****##
	##************************************************##
	
	_speed = SPEED;
	flow = 1; 			## 1 = Front move, -1 = Back move
	
	while x!=" ":
		x= getch()
			
		if x == "a":	#Front
			flow = 1;
			_speed = SPEED*flow
			print("FRONT..."+str(_speed));		
			
		elif x == "s":
			print("STOP... 0");
			setpoint.data[0]= 0;
			setpoint.data[1]= 0;
			pub_f.publish(setpoint);
			
		elif x == "d":
			flow=-1;
			_speed = SPEED*flow
			print("BACK..."+str(_speed));
			
		elif x == "i":	#Moving action
			print("Moving ...");
			setpoint.data[0]= _speed;
			setpoint.data[1]= _speed;
			pub_f.publish(setpoint);
			
		elif x == "j":
			print("Left action...");
			setpoint.data[0]= _speed;
			#setpoint.data[1]= _speed/4;
			setpoint.data[1]= -_speed;
			pub_f.publish(setpoint);
			
		elif x == "l":
			print("Rigth action...");
			#setpoint.data[0]= _speed/4;
			setpoint.data[0]= -_speed;
			setpoint.data[1]= _speed;
			pub_f.publish(setpoint);
			
		print(x)
		
	#Stop program	
	setpoint.data[0]= 0;
	setpoint.data[1]= 0;
	pub_f.publish(setpoint);
	file1.close()
	file2.close()
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
