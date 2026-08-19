import sys
import select
import termios
import tty

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Color
from std_msgs.msg import String


def get_key():
    """Read one key from the keyboard without requiring Enter."""
    settings = termios.tcgetattr(sys.stdin)

    try:
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(
            sys.stdin,
            termios.TCSADRAIN,
            settings
        )

    return key


class Controller(Node):

    def __init__(self):
        super().__init__('controller')

        # ROS2 PARAMETERS

        self.declare_parameter(
            'cmd_vel_topic',
            '/cmd_vel'
        )

        self.declare_parameter(
            'color_sensor_topic',
            '/turtle1/color_sensor'
        )

        self.declare_parameter(
            'dominant_color_topic',
            '/dominant_color'
        )

        self.cmd_vel_topic = self.get_parameter(
            'cmd_vel_topic'
        ).value

        self.color_sensor_topic = self.get_parameter(
            'color_sensor_topic'
        ).value

        self.dominant_color_topic = self.get_parameter(
            'dominant_color_topic'
        ).value

        # MOVEMENT PUBLISHER

        self.cmd_vel_pub = self.create_publisher(
            Twist,
            self.cmd_vel_topic,
            10
        )

        # COLOR SENSOR SUBSCRIBER

        self.color_sub = self.create_subscription(
            Color,
            self.color_sensor_topic,
            self.color_callback,
            10
        )

        # DOMINANT COLOR PUBLISHER

        self.color_pub = self.create_publisher(
            String,
            self.dominant_color_topic,
            10
        )

        # KEYBOARD TIMER

        self.timer = self.create_timer(
            0.1,
            self.keyboard_callback
        )

        self.get_logger().info(
            'Controller started. Use W/A/S/D to move the turtle.'
        )

    # KEYBOARD CONTROL

    def keyboard_callback(self):

        if select.select([sys.stdin], [], [], 0.1)[0]:
            key = get_key()
            self.move_turtle(key)

    # TURTLE MOVEMENT

    def move_turtle(self, key):

        msg = Twist()

        if key == 'w':
            msg.linear.x = 2.0
            msg.angular.z = 0.0

        elif key == 's':
            msg.linear.x = -2.0
            msg.angular.z = 0.0

        elif key == 'a':
            msg.linear.x = 0.0
            msg.angular.z = 2.0

        elif key == 'd':
            msg.linear.x = 0.0
            msg.angular.z = -2.0

        elif key == ' ':
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        else:
            return

        self.cmd_vel_pub.publish(msg)

    # STOP TURTLE

    def stop_turtle(self):

        msg = Twist()

        msg.linear.x = 0.0
        msg.angular.z = 0.0

        self.cmd_vel_pub.publish(msg)

    # COLOR SENSOR

    def color_callback(self, msg):

        if msg.r > msg.g and msg.r > msg.b:
            color = 'Red'

        elif msg.g > msg.r and msg.g > msg.b:
            color = 'Green'

        else:
            color = 'Blue'

        if not hasattr(self, 'last_color'):
            self.last_color = None

        if color != self.last_color:

            self.get_logger().info(
                f'Dominant color: {color}'
            )

            self.last_color = color

        color_msg = String()
        color_msg.data = color

        self.color_pub.publish(color_msg)


def main(args=None):

    rclpy.init(args=args)

    node = Controller()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.stop_turtle()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()