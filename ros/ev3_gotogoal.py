import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Point, Quaternion
from std_msgs.msg import Header
from std_msgs.msg import Float32MultiArray
import signal
import sys
import math
import numpy as np
import gogoal

class EV3GotogoalNode(Node):

    def __init__(self, goal_x, goal_y):
        super().__init__('ev3_gotogoal')
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.pursuer_pose_subscriber = self.create_subscription(PoseStamped, 'pursuer/pose', self.pursuer_callback, 10)
        print(self.pursuer_pose_subscriber)

        #self.yaw = None
        self.x = None
        #self.y = None
        self.publisher = self.create_publisher(Float32MultiArray, 'motor_commands', 10)
        print("test")
        self.create_timer(0.1, self.gotogoal)
        self.speed_ratios = []
        self.val = []


    def pursuer_callback(self, q):
        q_w, q_x, q_y, q_z = q.pose.orientation.x, q.pose.orientation.y, q.pose.orientation.z, q.pose.orientation.w
        self.x = q.pose.position.x
        self.y = q.pose.position.y
        if (abs(np.linalg.norm(self.x-self.goal_x))> 0.05 or abs(np.linalg.norm(self.y-self.goal_y))> 0.05):
            self.yaw = math.atan2(2 * (q_y * q_z + q_w * q_x), q_w**2 - q_x**2 - q_y**2 + q_z**2)
            ort = gogoal.OmniRobot(np.array([self.x,self.y]),self.yaw)
            self.val = ort.move_to_target(np.array([self.goal_x,self.goal_y]))
        else:
            self.val = [0,0,0]
    def gotogoal(self):
        msg = Float32MultiArray()
        msg.data = self.val 
        self.publisher.publish(msg)



def main(args=None):
    rclpy.init(args=args)
    goal_x = -0.7
    goal_y = 0.7
    gotogoal = EV3GotogoalNode(goal_x=goal_x, goal_y=goal_y)
    rclpy.spin(gotogoal)
    gotogoal.destroy_node()
    rclpy.shutdown()



def custom_handler(sig, frame):
    node = Node("simple_publisher")  
    pub = node.create_publisher(Float32MultiArray, 'motor_commands', 10)
    msg = Float32MultiArray()
    msg.data = [0,0,0] 
    pub.publish(msg)
    sys.exit(0)

signal.signal(signal.SIGINT, custom_handler)

if __name__ == "__main__":
    main()
