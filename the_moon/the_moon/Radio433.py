import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import threading
from pymavlink import mavutil

class Radio433(Node):
    def __init__(self, port: str, vehicle_type = "GS"):
        super().__init__('radio433')
        self.pings_sent_file = open(f'radio433_log_pings_sent_{vehicle_type}_{self.get_clock().now().to_msg().sec}.txt', 'a')
        self.msgs_received_file = open(f'radio433_log_msgs_received_{vehicle_type}_{self.get_clock().now().to_msg().sec}.txt', 'a')
        self.publisher_ = self.create_publisher(String, 'radio433_topic', 10)
        self.timer_heartbeat = self.create_timer(0.5, self.send_heartbeat)
        self.timer_ping = self.create_timer(0.1, self.send_ping)
        self.get_logger().info('Radio433 node has been started.')
        self.ping_seq = 0
    
        self.vehicle_type = ""
        if vehicle_type == "rocket":
            self.vehicle_type = mavutil.mavlink.MAV_TYPE_ROCKET
        elif vehicle_type == "GS":
            self.vehicle_type = mavutil.mavlink.MAV_TYPE_GCS
        else:
            self.vehicle_type = mavutil.mavlink.MAV_TYPE_GENERIC

        self.mavlink_connection = mavutil.mavlink_connection(port, baud=57600)
        self.receiving_thread = threading.Thread(target=self.receiving_loop)
        self.receiving_thread.start()

    def send_heartbeat(self):
        self.mavlink_connection.mav.heartbeat_send(
            self.vehicle_type,
            mavutil.mavlink.MAV_AUTOPILOT_INVALID,
            0,
            0,
            mavutil.mavlink.MAV_STATE_ACTIVE
        )
    
    def send_ping(self):
        # with open(f'radio433_log_pings_sent_{self.vehicle_type}_{self.get_clock().now().to_msg().sec}.txt', 'a') as log_file:
        time_usec = self.get_clock().now().to_msg().sec * 1_000_000 + self.get_clock().now().to_msg().nanosec // 1_000
        self.mavlink_connection.mav.ping_send(time_usec, self.ping_seq, 0, 0)
        self.pings_sent_file.write(f'{time_usec} {self.ping_seq}\n')
        self.pings_sent_file.flush()
        self.get_logger().info(f'Ps {self.ping_seq}')
        self.ping_seq = self.ping_seq + 1

    def receiving_loop(self):
        # with open(file_name, 'a') as log_file:
        while True:
            msg = self.mavlink_connection.recv_match(blocking=True)
            if msg.get_type() == 'RADIO_STATUS':
                rssi = msg.rssi
                noise = msg.noise
                SNR = rssi - noise
                rem_rssi = msg.remrssi
                rem_noise = msg.remnoise
                rem_SNR = rem_rssi - rem_noise
                self.get_logger().info(f'RADIO_STATUS: SNR={SNR}, remSNR={rem_SNR}, {rssi}/{noise}, rem {rem_rssi}/{rem_noise}')
                time_usec = self.get_clock().now().to_msg().sec * 1_000_000 + self.get_clock().now().to_msg().nanosec // 1_000
                log_line = f'S {time_usec} {SNR} {rem_SNR} {msg.rssi} {msg.remrssi} {msg.txbuf} {msg.noise} {msg.remnoise} {msg.rxerrors} {msg.fixed}\n'
                self.msgs_received_file.write(log_line)
                self.msgs_received_file.flush()
            elif msg.get_type() == 'PING':
                # save received message to file
                # if the adress is 0 also send response ping
                time_usec = self.get_clock().now().to_msg().sec * 1_000_000 + self.get_clock().now().to_msg().nanosec // 1_000
                log_line = f'P {time_usec} {msg.time_usec} {msg.seq} {msg.target_system} {msg.target_component}\n'
                self.get_logger().info(f'P {msg.seq}')
                self.msgs_received_file.write(log_line)
                if msg.target_system == 0:
                    self.mavlink_connection.mav.ping_send(time_usec, msg.seq, 1, 1)
                    self.get_logger().info(f'R {msg.seq}')
                self.msgs_received_file.flush()