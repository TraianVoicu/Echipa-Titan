#! /usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

def callback(msg):
    vel = Twist()
    front = min(msg.ranges[0], msg.ranges[1], msg.ranges[358], msg.ranges[359])
    left  = min(msg.ranges[85], msg.ranges[90], msg.ranges[95])
    right = min(msg.ranges[265], msg.ranges[270], msg.ranges[275])

    if front > 1.0:
        vel.linear.x  = 0.2
        vel.angular.z = 0.0

    if front < 1.0:
        vel.linear.x  = 0.0
        vel.angular.z = 0.5

    if right < 1.0:
        vel.linear.x  = 0.0
        vel.angular.z = 0.5

    if left < 1.0:
        vel.linear.x  = 0.0
        vel.angular.z = -0.5

    pub.publish(vel)

rospy.init_node('wall_avoidance_node')
sub = rospy.Subscriber('/scan', LaserScan, callback)
rospy.spin()
