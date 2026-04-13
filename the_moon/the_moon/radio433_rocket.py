import rclpy
from the_moon.Radio433 import Radio433

def main():
    rclpy.init()
    radio433_node = Radio433('/dev/ttyUSB1', "rocket")
    rclpy.spin(radio433_node)
    radio433_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
