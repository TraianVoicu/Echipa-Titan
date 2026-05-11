#!/usr/bin/env python3
import rospy
from triangle_movement.srv import Triangle

def triangle_client(side, repetitions):
    rospy.wait_for_service('move_triangle')
    try:
        move = rospy.ServiceProxy('move_triangle', Triangle)
        resp = move(side, repetitions)
        rospy.loginfo(f"Success: {resp.success}")
        return resp.success
    except rospy.ServiceException as e:
        rospy.logerr(f"Eroare: {e}")

if __name__ == '__main__':
    rospy.init_node('triangle_client')
    triangle_client(side=1.0, repetitions=2)
