#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool

class NumberCounter(Node):
    def __init__(self):
        super().__init__("number_counter")
        self.counter_ = 0

        # Subscriber
        self.subscriber_ = self.create_subscription(
            Int64,
            "number",
            self.callback_number,
            10
        )

        # Publisher
        self.publisher_ = self.create_publisher(
            Int64,
            "number_count",
            10
        )

        # Service Server
        self.server_ = self.create_service(
            SetBool,
            "reset_counter",
            self.callback_reset_counter
        )

        self.get_logger().info("Number Counter with Reset Service started")

    def callback_number(self, msg):
        self.counter_ += msg.data
        out_msg = Int64()
        out_msg.data = self.counter_
        self.publisher_.publish(out_msg)
        self.get_logger().info(f"Counter updated: {out_msg.data}")

    def callback_reset_counter(self, request, response):
        if request.data:
            self.counter_ = 0
            response.success = True
            response.message = "Counter reset to zero."
            self.get_logger().info("Counter reset to zero.")
        else:
            response.success = False
            response.message = "Request data was false. Counter not reset."
            self.get_logger().warn("Reset request ignored (data=false).")

        return response

def main(args=None):
    rclpy.init(args=args)
    node = NumberCounter()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
