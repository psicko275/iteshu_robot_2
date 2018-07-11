#!/usr/bin/env python  
import roslib
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv

if __name__ == '__main__':
    rospy.init_node('tf_turtle')

    listener = tf.TransformListener()#creo el tf listener 

    rospy.wait_for_service('spawn')#eperar ujn servicio spawn
    spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    spawner(4, 2, 0, 'turtle2')

    turtle_vel = rospy.Publisher('turtle2/cmd_vel', geometry_msgs.msg.Twist,queue_size=1)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/turtle2', '/turtle1', rospy.Time(0))#listener de una transformacion entre 2 y 1
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        angular = 4 * math.atan2(trans[1], trans[0])#velocidad angle posicion en x y y de la tortuga 1
        linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)#
        cmd = geometry_msgs.msg.Twist()#meter los 2 datos en un twist
        cmd.linear.x = linear
        cmd.angular.z = angular
        turtle_vel.publish(cmd)#publicar en turtle 2

        rate.sleep()
