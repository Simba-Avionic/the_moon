import time
import threading
import os
import logging
from collections import deque
from pymavlink import mavutil

import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Radio433:
    def __init__(self, port: str, vehicle_type="GS"):
        self.logger = logging.getLogger(self.__class__.__name__)
        os.makedirs('logs', exist_ok=True)
        
        current_sec = int(time.time())
        self.pings_sent_file = open(f'logs/radio433_log_pings_sent_{vehicle_type}_{current_sec}.txt', 'a')
        self.msgs_received_file = open(f'logs/radio433_log_msgs_received_{vehicle_type}_{current_sec}.txt', 'a')
        
        self.logger.info('Radio433 node has been started.')
        self.ping_seq = 0
        self.running = True
        self.start_time = time.time()
        
        # --- Live Plotting Data Buffers ---
        # Deque automatically drops the oldest items when maxlen is reached
        self.max_points = 100 
        self.plot_times = deque(maxlen=self.max_points)
        self.plot_snr = deque(maxlen=self.max_points)
        self.plot_rem_snr = deque(maxlen=self.max_points)
    
        self.vehicle_type = ""
        if vehicle_type == "rocket":
            self.vehicle_type = mavutil.mavlink.MAV_TYPE_ROCKET
        elif vehicle_type == "GS":
            self.vehicle_type = mavutil.mavlink.MAV_TYPE_GCS
        else:
            self.vehicle_type = mavutil.mavlink.MAV_TYPE_GENERIC

        self.logger.info(f"Connecting to MAVLink on port: {port} at 115200 / 57600 baud")
        self.mavlink_connection = mavutil.mavlink_connection(port, baud=57600)
        
        # Start background threads
        self.receiving_thread = threading.Thread(target=self.receiving_loop, daemon=True)
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.ping_thread = threading.Thread(target=self._ping_loop, daemon=True)

        self.receiving_thread.start()
        self.heartbeat_thread.start()
        self.ping_thread.start()

    def _heartbeat_loop(self):
        while self.running:
            self.send_heartbeat()
            time.sleep(0.5)

    def _ping_loop(self):
        while self.running:
            self.send_ping()
            time.sleep(0.1)

    def send_heartbeat(self):
        self.mavlink_connection.mav.heartbeat_send(
            self.vehicle_type,
            mavutil.mavlink.MAV_AUTOPILOT_INVALID,
            0,
            0,
            mavutil.mavlink.MAV_STATE_ACTIVE
        )
    
    def send_ping(self):
        time_usec = time.time_ns() // 1_000
        self.mavlink_connection.mav.ping_send(time_usec, self.ping_seq, 0, 0)
        self.pings_sent_file.write(f'{time_usec} {self.ping_seq}\n')
        self.pings_sent_file.flush()
        self.ping_seq += 1

    def receiving_loop(self):
        while self.running:
            msg = self.mavlink_connection.recv_match(blocking=True)
            if not msg:
                continue

            msg_type = msg.get_type()
            
            if msg_type == 'RADIO_STATUS':
                rssi = msg.rssi
                noise = msg.noise
                SNR = rssi - noise
                rem_rssi = msg.remrssi
                rem_noise = msg.remnoise
                rem_SNR = rem_rssi - rem_noise
                
                self.logger.info(f'RADIO_STATUS: SNR={SNR}, {rssi}/{noise} | remSNR={rem_SNR} rem {rem_rssi}/{rem_noise}')
                
                # Save plot data (relative time in seconds)
                rel_time = time.time() - self.start_time
                self.plot_times.append(rel_time)
                self.plot_snr.append(SNR)
                self.plot_rem_snr.append(rem_SNR)
                
                # File logging
                time_usec = time.time_ns() // 1_000
                log_line = f'S {time_usec} {SNR} {rem_SNR} {msg.rssi} {msg.remrssi} {msg.txbuf} {msg.noise} {msg.remnoise} {msg.rxerrors} {msg.fixed}\n'
                self.msgs_received_file.write(log_line)
                self.msgs_received_file.flush()
            
            elif msg_type == 'PING':
                time_usec = time.time_ns() // 1_000
                log_line = f'P {time_usec} {msg.time_usec} {msg.seq} {msg.target_system} {msg.target_component}\n'
                self.msgs_received_file.write(log_line)
                
                if msg.target_system == 0:
                    self.mavlink_connection.mav.ping_send(time_usec, msg.seq, 1, 1)
                self.msgs_received_file.flush()

    def stop(self):
        self.logger.info("Initiating shutdown...")
        self.running = False
        self.pings_sent_file.close()
        self.msgs_received_file.close()
        self.logger.info("Shutdown complete. Files closed.")


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    TARGET_PORT = '/dev/ttyUSB1'
    TARGET_VEHICLE = 'GS'
    
    radio = Radio433(port=TARGET_PORT, vehicle_type=TARGET_VEHICLE)
    
    # --- Matplotlib Live Plot Setup ---
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_title('Live 433MHz Telemetry')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('SNR')
    ax.grid(True)
    
    line_snr, = ax.plot([], [], label='Local SNR', color='blue', marker='.')
    line_rem_snr, = ax.plot([], [], label='Remote SNR', color='orange', marker='.')
    ax.legend(loc='upper right')

    def update_plot(frame):
        # Only update if we have data
        if not radio.plot_times:
            return line_snr, line_rem_snr
        
        # Create a shallow copy to avoid "RuntimeError: deque mutated during iteration"
        times = list(radio.plot_times)
        snrs = list(radio.plot_snr)
        rem_snrs = list(radio.plot_rem_snr)
        
        line_snr.set_data(times, snrs)
        line_rem_snr.set_data(times, rem_snrs)
        
        # Dynamically rescale the axes to fit new data
        ax.relim()
        ax.autoscale_view()
        
        return line_snr, line_rem_snr

    # Update the plot every 500 milliseconds
    ani = animation.FuncAnimation(fig, update_plot, interval=500, cache_frame_data=False)
    
    logging.info("Starting live plot. Close the plot window to stop the script.")
    
    try:
        # plt.show() is blocking. It replaces the infinite while loop!
        plt.show()
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received.")
    finally:
        radio.stop()