#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute

class TeleportClient(Node):
    def __init__(self):
        super().__init__("teleport_client")
        self.client = self.create_client(TeleportAbsolute, "/turtle1/teleport_absolute")

    def send_request(self):
        while not self.client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for teleport service...")

        req = TeleportAbsolute.Request()
        req.x = 2.0
        req.y = 9.0
        req.theta = 0.0

        future = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        self.get_logger().info("Teleport done!")

def main():
    rclpy.init()
    node = TeleportClient()
    node.send_request()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

