import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import numpy as np

class PoseListener(Node):
    def __init__(self):
        super().__init__('pose_listener')
        self.pursuer1_sub = self.create_subscription(PoseStamped, 'pursuer1/pose', self.pursuer1_callback, 10)
        self.pursuer2_sub = self.create_subscription(PoseStamped, 'pursuer2/pose', self.pursuer2_callback, 10)
        self.evader_sub = self.create_subscription(PoseStamped, 'evader/pose', self.evader_callback, 10)


        self.pur_pos = np.full((2, 2), np.nan)  
        self.ev_pos = np.full((1, 2), np.nan) 

    def pursuer1_callback(self, msg):
        self.pur_pos[0] = [msg.pose.position.x, msg.pose.position.y]
        self.get_logger().info(f"Received Pursuer 1 Position: {self.pur_pos[0]}")

    def pursuer2_callback(self, msg):
        self.pur_pos[1] = [msg.pose.position.x, msg.pose.position.y]
        self.get_logger().info(f"Received Pursuer 2 Position: {self.pur_pos[1]}")

    def evader_callback(self, msg):
        self.ev_pos[0] = [msg.pose.position.x, msg.pose.position.y]
        self.get_logger().info(f"Received Evader Position: {self.ev_pos[0]}")
        
def get_positions():
    rclpy.init()
    node = PoseListener()
    while np.isnan(node.pur_pos).any() or np.isnan(node.ev_pos).any():
        rclpy.spin_once(node)

    pursuer_positions = node.pur_pos
    evader_position = node.ev_pos
    print(pursuer_positions)
    node.destroy_node()
    rclpy.shutdown()

    return pursuer_positions, evader_position
