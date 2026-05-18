#!/usr/bin/env python3

import rospy
import actionlib
from ardrone_action_Lucian_Curea_Traian_Voicu.msg import (
    DroneActionAction,
    DroneActionFeedback,
    DroneActionResult,
)
from std_msgs.msg import Empty


NUME_ECHIPA = "Lucian_Curea_Traian_Voicu"


class DroneActionServer:
    def __init__(self):
        
        self._action_name = "drone_action_" + NUME_ECHIPA
        self._as = actionlib.SimpleActionServer(
            self._action_name,
            DroneActionAction,
            execute_cb=self.execute_callback,
            auto_start=False,
        )

       
        self._takeoff_pub = rospy.Publisher("/ardrone/takeoff", Empty, queue_size=1)
        self._land_pub = rospy.Publisher("/ardrone/land", Empty, queue_size=1)

        
        self._feedback = DroneActionFeedback()
        self._result = DroneActionResult()

        self._as.start()
        rospy.loginfo(
            "Action Server [%s] pornit. Echipa: %s", self._action_name, NUME_ECHIPA
        )

    def execute_callback(self, goal):
        rospy.loginfo("Goal primit: %s", goal.goal_command)

        rate = rospy.Rate(1)  # 1 Hz - publicare feedback o dată pe secundă
        success = True

        command = goal.goal_command.upper().strip()

        if command == "TAKEOFF":
            
            self._takeoff_pub.publish(Empty())
            rospy.loginfo("Drona decoleaza...")

            
            while not rospy.is_shutdown():
                if self._as.is_preempt_requested():
                    rospy.loginfo("Goal preemptat")
                    self._as.set_preempted()
                    success = False
                    break

                self._feedback.current_action = "TAKING OFF"
                self._as.publish_feedback(self._feedback)
                rate.sleep()

        elif command == "LAND":
            
            self._land_pub.publish(Empty())
            rospy.loginfo("Drona aterizeaza...")

            
            for i in range(5):
                if self._as.is_preempt_requested():
                    self._as.set_preempted()
                    success = False
                    break

                self._feedback.current_action = "LANDING"
                self._as.publish_feedback(self._feedback)
                rate.sleep()

        else:
            rospy.logwarn("Comanda necunoscuta: %s", command)
            self._as.set_aborted()
            return

        if success:
            
            rospy.loginfo("Actiune finalizata cu succes")
            self._as.set_succeeded(self._result.result)


if __name__ == "__main__":
    rospy.init_node("drone_action_server_" + NUME_ECHIPA)
    server = DroneActionServer()
    rospy.spin()
