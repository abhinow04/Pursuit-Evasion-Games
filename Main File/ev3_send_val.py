import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

class EV3SendCommands(Node):

    def __init__(self, robot, w_vel):
        super().__init__('ev3_send_commands')
        self.publisher = self.create_publisher(Float32MultiArray, f'{robot}/motor_commands', 10)
        self.send_velocity(w_vel)

    def send_velocity(self, w_vel):
        msg = Float32MultiArray()
        msg.data = w_vel
        self.publisher.publish(msg)
        print("done")
        self.get_logger().info(f'Published velocity: {w_vel} to {self.publisher.topic}')

def send_vel(robot_name, velocity_data):
    rclpy.init()
    node = EV3SendCommands(robot_name, velocity_data)
    
    rclpy.spin_once(node, timeout_sec=0.1)

    node.destroy_node()
    rclpy.shutdown()
