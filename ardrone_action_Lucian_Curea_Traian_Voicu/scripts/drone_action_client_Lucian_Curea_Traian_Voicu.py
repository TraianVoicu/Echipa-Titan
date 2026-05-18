#!/usr/bin/env python3

import rospy
import actionlib
import sys
from ardrone_action_Lucian_Curea_Traian_Voicu.msg import (
    DroneActionAction,
    DroneActionGoal,
)

NUME_ECHIPA = "Lucian_Curea_Traian_Voicu"


def feedback_callback(feedback):
    rospy.loginfo("Feedback: %s", feedback.current_action)


def send_goal(command):
    client = actionlib.SimpleActionClient(
        "drone_action_" + NUME_ECHIPA, DroneActionAction
    )

    rospy.loginfo("Traian si Lucian astepta comenzi...")
    client.wait_for_server()

    goal = DroneActionGoal()
    goal.goal_command = command

    rospy.loginfo("Trimit goal: %s", command)
    client.send_goal(goal, feedback_cb=feedback_callback)

    
    if command.upper() == "LAND":
        client.wait_for_result()
        rospy.loginfo("Aterizare finalizata")


if __name__ == "__main__":
    rospy.init_node("drone_action_client_" + NUME_ECHIPA)

    if len(sys.argv) < 2:
        print("Utilizare: rosrun ardrone_action_Lucian_Curea_Traian_Voicu drone_action_client_Lucian_Curea_Traian_Voicu.py [TAKEOFF|LAND]")
        sys.exit(1)

    send_goal(sys.argv[1])
