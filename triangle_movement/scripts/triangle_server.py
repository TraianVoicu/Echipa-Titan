#!/usr/bin/env python3
import rospy
import math
from geometry_msgs.msg import Twist
from triangle_movement.srv import Triangle, TriangleResponse

def move_triangle(side, repetitions):
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)
    speed = 0.2
    turn_speed = 0.5
    side_time = side / speed
    turn_time = (2 * math.pi / 3) / turn_speed
    twist = Twist()

    for _ in range(repetitions):
        for _ in range(3):
            twist.linear.x = speed
            twist.angular.z = 0.0
            end = rospy.Time.now() + rospy.Duration(side_time)
            while rospy.Time.now() < end:
                pub.publish(twist)
                rate.sleep()

            twist.linear.x = 0.0
            twist.angular.z = turn_speed
            end = rospy.Time.now() + rospy.Duration(turn_time)
            while rospy.Time.now() < end:
                pub.publish(twist)
                rate.sleep()

    twist.linear.x = 0.0
    twist.angular.z = 0.0
    pub.publish(twist)
    return True

def handle_request(req):
    rospy.loginfo(f"Triunghi: side={req.side}, repetitions={req.repetitions}")
    success = move_triangle(req.side, req.repetitions)
    return TriangleResponse(success=success)

def triangle_server():
    rospy.init_node('triangle_server')
    rospy.Service('move_triangle', Triangle, handle_request)
    rospy.loginfo("Server pornit, astept cereri...")
    rospy.spin()

if __name__ == '__main__':
    triangle_server()
