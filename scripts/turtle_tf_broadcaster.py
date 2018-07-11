#!/usr/bin/env python  
import roslib

import rospy

import tf
import turtlesim.msg

def handle_turtle_pose(msg, turtlename):#recibir dato y guardar valores
    br = tf.TransformBroadcaster()#guardar en una transformacion
    br.sendTransform((msg.x, msg.y, 0),#en x,y,z
                     tf.transformations.quaternion_from_euler(0, 0, msg.theta),#dato estandar cuaternion de roll pitch yaw
                     rospy.Time.now(),
                     turtlename,#nombre del marco de referencia movil y fijo
                     "world")

if __name__ == '__main__':
    rospy.init_node('turtle_tf_broadcaster')
    turtlename = rospy.get_param('~turtle')
    rospy.Subscriber('/%s/pose' % turtlename,
                     turtlesim.msg.Pose,
                     handle_turtle_pose,
                     turtlename)
    rospy.spin()
