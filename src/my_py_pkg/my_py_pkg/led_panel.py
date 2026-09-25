#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import LedStateArray
from my_robot_interfaces.srv import SetLed

class LEDPanelNode(Node):
    def __init__(self):
        super().__init__("led_panel")
        self.declare_parameter("led_states", [0, 0, 0])
        self.led_states = self.get_parameter("led_states").value
        self.led_states_pub = self.create_publisher(
            LedStateArray, "led_panel_state", 10)
        self.led_states_timer = self.create_timer(
            5.0, self.publish_led_states)
        self.set_led_service = self.create_service(
            SetLed, "set_led", self.callback_set_led)
        self.get_logger().info("LED panel node has been started.")

    def publish_led_states(self):
        msg = LedStateArray()
        msg.led_states = self.led_states
        self.led_states_pub.publish(msg)

    def callback_set_led(self, request: SetLed.Request, response: SetLed.Response):
        led_number = request.led_number
        state = request.state

        if led_number >= len(self.led_states) or led_number < 0:
            response.success = False
            return response

        if state not in [0, 1]:
            response.success = False
            return response

        self.led_states[led_number] = state
        response.success = True
        return response

def main(args=None):
    rclpy.init(args=args)
    node = LEDPanelNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
