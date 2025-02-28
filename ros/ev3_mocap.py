import motioncapture
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Point, Quaternion
from std_msgs.msg import Header

class EV3_MocapNode(Node):
    def __init__(self):
        super().__init__('ev3_mocap')
        self.pursuer_publisher = self.create_publisher(PoseStamped, "pursuer/pose", 10)
        self.evader1_publisher = self.create_publisher(PoseStamped, "evader1/pose", 10)
        self.evader2_publisher = self.create_publisher(PoseStamped, "evader2/pose", 10)

        timer_period = 1 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.mc = motioncapture.connect('vrpn', {"hostname":"10.21.2.252", "port" : "3883"})
        
    def timer_callback(self):
        msg = PoseStamped()
        msg.pose.position = Point()
        msg.pose.orientation = Quaternion()
        self.mc.waitForNextFrame()
        print(self.mc.rigidBodies.keys())
        for name, obj in self.mc.rigidBodies.items():
            position = list(obj.position)
            msg.header.frame_id = str(name)
            msg.pose.position.x = float(position[0])
            msg.pose.position.y = float(position[1])
            msg.pose.position.z = float(position[2])
            msg.pose.orientation.x = obj.rotation.x
            msg.pose.orientation.y = obj.rotation.y
            msg.pose.orientation.z = obj.rotation.z
            msg.pose.orientation.w = obj.rotation.w
            print(position)
            if str(name) == "pursuer":
                self.pursuer_publisher.publish(msg)
                self.get_logger().info('Publishing: "{}":"{}" "{}"'.format(msg.header.frame_id, msg.pose.position, msg.pose.orientation))
                print(msg)
            elif str(name) == "evader1":
                self.evader1_publisher.publish(msg)
                self.get_logger().info('Publishing: "{}":"{}" "{}"'.format(msg.header.frame_id, msg.pose.position, msg.pose.orientation))
            elif str(name) == "evader2":
                self.evader2_publisher.publish(msg)
                self.get_logger().info('Publishing: "{}":"{}" "{}"'.format(msg.header.frame_id, msg.pose.position, msg.pose.orientation))



def main(args=None):
    rclpy.init(args=args)
    mocap = EV3_MocapNode()
    rclpy.spin(mocap)
    mocap.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
