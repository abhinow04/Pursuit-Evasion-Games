import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Point, Quaternion
from std_msgs.msg import Header
from std_msgs.msg import Float32MultiArray

import sys
import math
import numpy as np
import gogoal
import matplotlib.pyplot as plt
class EV3GotogoalNode(Node):

    def __init__(self, goal_x, goal_y):
        super().__init__('ev3_gotogoal')
        self.pursuer1_pose_subscriber = self.create_subscription(PoseStamped, 'pursuer0/pose', self.pursuer_callback, 10)
        self.pursuer2_pose_subscriber = self.create_subscription(PoseStamped, 'pursuer1/pose', self.pursuer_callback, 10)
        self.evader_pose_subscriber = self.create_subscription(PoseStamped,'evader/pose',self.pursuer_callback,10)
        print(self.pursuer_pose_subscriber)
    

        self.publisher = self.create_publisher(Float32MultiArray, 'motor_commands', 10)
        print("test")
        self.create_timer(0.1, self.gotogoal)
        self.speed_ratios = []
        self.val = []


##    def pursuer_callback(self, q):
##        q_w, q_x, q_y, q_z = q.pose.orientation.x, q.pose.orientation.y, q.pose.orientation.z, q.pose.orientation.w
##        self.x = q.pose.position.x
##        self.y = q.pose.position.y
##        if (abs(np.linalg.norm(self.x-self.goal_x))> 0.08 or abs(np.linalg.norm(self.y-self.goal_y))> 0.08):
##            self.yaw = math.atan2(2 * (q_y * q_z + q_w * q_x), q_w**2 - q_x**2 - q_y**2 + q_z**2)

        
##        else:
##            self.val = [0,0,0]

    def gotogoal(self):
        msg = Float32MultiArray()
        msg.data = self.val 
        self.publisher.publish(msg)



    
def send_wheel_velocities(pursuer_wheel_vels, evader_wheel_vels):
    rclpy.init()
    node = Node("wheel_velocity_publisher")
    pub = node.create_publisher(Float32MultiArray, 'motor_commands', 10)

    msg = Float32MultiArray()
    msg.data = pursuer_wheel_vels + evader_wheel_vels
    pub.publish(msg)

    print("Sent wheel velocities:", msg.data)

    node.destroy_node()
    rclpy.shutdown()


def send_wheel_velocities(robot,vel):
    rclpy.init()
    node = Node("wheel_velocity_publisher")
    pub = node.create_publisher(Float32MultiArray, f'{robot}/motor_commands', 10)
    msg = Float32MultiArray()
    msg.data = vel
    pub.publish(msg)

    print("Sent wheel velocities:", msg.data)

    node.destroy_node()
    rclpy.shutdown()


