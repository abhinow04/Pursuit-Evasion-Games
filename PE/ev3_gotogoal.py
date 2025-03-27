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
import matplotlib.pyplot as plt
class EV3GotogoalNode(Node):

    def __init__(self, goal_x, goal_y):
        super().__init__('ev3_gotogoal')
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.pursuer1_pose_subscriber = self.create_subscription(PoseStamped, 'pursuer1/pose', self.pursuer1_callback, 10)
        self.pursuer2_pose_subscriber = self.create_subscription(PoseStamped, 'pursuer2/pose', self.pursuer2_callback, 10)
        self.evader_pose_subscriber = self.create_subscription(PoseStamped, 'evader/pose', self.evader_callback, 10)
        print(self.pursuer1_pose_subscriber)
        print(self.pursuer2_pose_subscriber)
        print(self.evader_pose_subscriber)
        
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
        if (abs(np.linalg.norm(self.x-self.goal_x))> 0.08 or abs(np.linalg.norm(self.y-self.goal_y))> 0.08):
            self.yaw = math.atan2(2 * (q_y * q_z + q_w * q_x), q_w**2 - q_x**2 - q_y**2 + q_z**2)
            ort = gogoal.OmniRobot(np.array([self.x,self.y]),self.yaw)
            self.val = ort.move_to_target(np.array([self.goal_x,self.goal_y]))

        else:
            self.val = [0,0,0]

    def gotogoal(self):
        msg = Float32MultiArray()
        msg.data = self.val 
        self.publisher.publish(msg)



##def main(args=None):
##    rclpy.init(args=args)
##    goal_x = -0.7
##    goal_y = 0.7
##    gotogoal = EV3GotogoalNode(goal_x=goal_x, goal_y=goal_y)
##    rclpy.spin(gotogoal)
##    gotogoal.destroy_node()
##    rclpy.shutdown()



def custom_handler(sig, frame):
    node = Node("simple_publisher")  
    pub = node.create_publisher(Float32MultiArray, 'motor_commands', 10)
    msg = Float32MultiArray()
    msg.data = [0,0,0] 
    pub.publish(msg)
    sys.exit(0)

def send_wheel_velocities(pursuer_wheel_vels, evader_wheel_vels,ind):
    rclpy.init()
    print(ind)  
    node = Node("wheel_velocity_publisher")
    pub = node.create_publisher(Float32MultiArray, 'pursuer1/motor_commands', 10)
    msg = Float32MultiArray()
    print(pursuer_wheel_vels)
    msg.data = pursuer_wheel_vels[0]
    evader_wheel_vels
    pub.publish(msg)

    print("Sent wheel velocities:", msg.data)

    node.destroy_node()
    rclpy.shutdown()


signal.signal(signal.SIGINT, custom_handler)

##if __name__ == "__main__":
##    main()
