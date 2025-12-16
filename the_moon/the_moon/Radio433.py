import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import threading
from pymavlink import mavutil

class Radio433(Node):
    def __init__(self):
        super().__init__('radio433')
        self.publisher_ = self.create_publisher(String, 'radio433_topic', 10)
        self.timer_heartbeat = self.create_timer(0.5, self.send_heartbeat)
        self.get_logger().info('Radio433 node has been started.')
        self.i = 0
        self.mavlink_connection = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600)
        self.receiving_thread = threading.Thread(target=self.receiving_loop)
        self.receiving_thread.start()
    
    def send_heartbeat(self):
        self.mavlink_connection.mav.heartbeat_send(
            mavutil.mavlink.MAV_TYPE_GCS,
            mavutil.mavlink.MAV_AUTOPILOT_INVALID,
            0,
            0,
            mavutil.mavlink.MAV_STATE_ACTIVE
        )
        
    def receiving_loop(self):
        while True:
            msg = self.mavlink_connection.recv_match(blocking=True)
            if msg:
                self.get_logger().info(f'Received MAVLink message: {msg}')