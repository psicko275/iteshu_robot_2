import rospy
from std_msgs.msg import Bool

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('botton', anonymous=True)

    rospy.Subscriber('botton', Bool, callback)

    # spin() simply keeps python from exiting until this node is stopped
    botton=0
    rospy.spin()


if __name__ == '__main__':
    listener()
