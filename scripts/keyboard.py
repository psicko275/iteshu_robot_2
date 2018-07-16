#!/usr/bin/env python
import roslib;
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from copy import deepcopy
from visualization_msgs.msg._Marker import Marker
from visualization_msgs.msg._MarkerArray import MarkerArray
import tf
import sys, select, termios, tty

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

+/- : increase/decrease max speeds by 10%

anything else : stop

CTRL-C to quit
"""
#(linear x, angular z)
moveBindings = {
    'i':( 1,  0),
    'o':( 1, -1),
    'l':( 0, -1),
    '.':(-1,  1),
    ',':(-1,  0),
    'm':(-1,  1),
    'j':( 0,  1),
    'u':( 1,  1),
    'k':( 0,  0),
       }

speedBindings = {#To change the speed
    '+':(1.1, 1.1),
    '-':(.9, .9),
      }

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

speed = 0.1 #[m/sec] 
turn = 0.1 #[rad/sec]

def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed, turn)

if __name__ == "__main__":
    settings = termios.tcgetattr(sys.stdin)
    rospy.init_node('teleop_twist_keyboard')
    """ ROS Parameters
    """
    vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    x = 0
    th = 0
    status = 0
    try:
        print msg
        print vels(speed, turn)
        key_vel = Twist()
        while(1):
            key = getKey()
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                th = moveBindings[key][1]
                key_vel.linear.x = x * speed; key_vel.linear.y = 0; key_vel.linear.z = 0
                key_vel.angular.x = 0; key_vel.angular.y = 0; key_vel.angular.z = th * turn
                vel_pub.publish(key_vel)
                print key_vel
                
            elif key in speedBindings.keys():
                speed = speed * speedBindings[key][0]
                turn = turn * speedBindings[key][1]

                print vels(speed, turn)
                if (status == 14):
                    print msg
                status = (status + 1) % 15
           
            else:
                x = 0; th = 0
                dir_x = -1; dir_th = 0 #dir_x=-1 means this is not a valid key to give directions
                if (key == '\x03'):
                    break



    except:
        rospy.loginfo("keyboard.py: exception")

    finally:
        key_vel = Twist()
       
        key_vel.linear.x = 0; key_vel.linear.y = 0; key_vel.linear.z = 0
        key_vel.angular.x = 0; key_vel.angular.y = 0; key_vel.angular.z = 0
        vel_pub.publish(key_vel)
        print key_vel
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
