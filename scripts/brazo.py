#!/usr/bin/env python


import rospy
from std_msgs.msg import Int16
        

def callback(data):
        global Codo Arriba
        global Codo Abajo
        
        
def talker():
    
    angle=UInt16() #angle should be between 0 and 180
    pub = rospy.Publisher('servo1', Int16, queue_size=10)
    #servos del brazo
    pub1 = rospy.Publisher('theta1',Int16, queue_size=10)
    pub2 = rospy.Publisher('theta2',Int16, queue_size=10)
    pub3 = rospy.Publisher('theta3',Int16, queue_size=10)
    pub4 = rospy.Publisher('theta4',Int16, queue_size=10)

    #suscritores a servos
    rospy.Subscriber('theta1',int16, callback)
    rospy.Subscriber('theta2',int16, callback)
    rospy.Subscriber('theta3',int16, callback)
    rospy.Subscriber('theta4',int16, callback)

    rospy.init_node('brazo', anonymous=True)

    rate = rospy.Rate(1) # 1hz
    theta1=0
    theta2=0
    theta3=0
    theta4=0
    global Codo Abajo = 0
    global Codo Arriba = 0
    while not rospy.is_shutdown(): 

        if servo1==0:
            servo1=20
            angle.data = servo1
            pub.publish(angle) 
            rate.sleep()
        else:
            pass
           
        

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

