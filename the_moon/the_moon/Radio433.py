import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Radio433(Node):
    def __init__(self):
        super().__init__('radio433')
        self.publisher_ = self.create_publisher(String, 'radio433_topic', 10)
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info('Radio433 node has been started.')
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Radio433 message {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1
        