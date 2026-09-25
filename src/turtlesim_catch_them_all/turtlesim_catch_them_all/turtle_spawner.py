#!/usr/init/env python3
import rclpy
from rclpy.node import Node
from functools import partial
import random
import math

from turtlesim.srv import Spawn
from turtlesim.srv import Kill
from my_robot_interfaces.msg import Turtle
from my_robot_interfaces.msg import TurtleArray
from my_robot_interfaces.srv import CatchTurtle


class TurtleSpawnerNode(Node):
    def __init__(self):
        super().__init__("turtle_spawner")

        # Parameters matching screenshot
        self.declare_parameter("turtle_name_prefix", "turtle")
        self.declare_parameter("spawn_frequency", 1.0)

        self.turtle_name_prefix_ = self.get_parameter("turtle_name_prefix").value
        self.spawn_frequency_ = self.get_parameter("spawn_frequency").value
        
        self.turtle_counter_ = 0
        self.alive_turtles_ = []

        # Publisher for alive turtles
        self.alive_turtles_publisher_ = self.create_publisher(
            TurtleArray, "alive_turtles", 10
        )

        # Spawn service client
        self.spawn_client_ = self.create_client(Spawn, "/spawn")

        # Kill service client
        self.kill_client_ = self.create_client(Kill, "/kill")

        # Catch turtle service
        self.catch_turtle_service_ = self.create_service(
            CatchTurtle, "catch_turtle", self.callback_catch_turtle
        )

        # Timer to spawn turtles periodically based on frequency
        self.spawn_turtle_timer_ = self.create_timer(
            1.0 / self.spawn_frequency_, self.spawn_new_turtle
        )

    # ---------------------------------------------------------
    # Catch turtle service callback
    # ---------------------------------------------------------
    def callback_catch_turtle(self, request: CatchTurtle.Request, response: CatchTurtle.Response):
        turtle_name = request.name
        self.call_kill_service(turtle_name)
        response.success = True
        return response

    # ---------------------------------------------------------
    # Publish alive turtles list
    # ---------------------------------------------------------
    def publish_alive_turtles(self):
        msg = TurtleArray()
        msg.turtles = self.alive_turtles_
        self.alive_turtles_publisher_.publish(msg)

    # ---------------------------------------------------------
    # Timer callback: spawn a new turtle
    # ---------------------------------------------------------
    def spawn_new_turtle(self):
        self.turtle_counter_ += 1
        name = self.turtle_name_prefix_ + str(self.turtle_counter_)

        x = random.uniform(0.0, 11.0)
        y = random.uniform(0.0, 11.0)
        theta = random.uniform(0.0, 2 * math.pi)

        self.call_spawn_service(name, x, y, theta)

    # ---------------------------------------------------------
    # Call /spawn service asynchronously
    # ---------------------------------------------------------
    def call_spawn_service(self, turtle_name, x, y, theta):
        while not self.spawn_client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for /spawn service...")

        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = turtle_name

        future = self.spawn_client_.call_async(request)
        future.add_done_callback(
            partial(self.callback_call_spawn_service, request=request)
        )

    # ---------------------------------------------------------
    # Callback when spawn service completes
    # ---------------------------------------------------------
    def callback_call_spawn_service(self, future, request):
        response = future.result()

        if response is None:
            self.get_logger().error("Spawn service failed!")
            return

        if response.name != "":
            self.get_logger().info(f"New alive turtle: {response.name}")

            new_turtle = Turtle()
            new_turtle.name = response.name
            new_turtle.x = request.x
            new_turtle.y = request.y
            new_turtle.theta = request.theta

            self.alive_turtles_.append(new_turtle)
            self.publish_alive_turtles()
        else:
            self.get_logger().warn("Spawn returned empty name!")

    # ---------------------------------------------------------
    # Call /kill service asynchronously
    # ---------------------------------------------------------
    def call_kill_service(self, turtle_name):
        while not self.kill_client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for /kill service...")

        request = Kill.Request()
        request.name = turtle_name

        future = self.kill_client_.call_async(request)
        future.add_done_callback(
            partial(self.callback_call_kill_service, turtle_name=turtle_name)
        )

    # ---------------------------------------------------------
    # Callback when kill service completes
    # ---------------------------------------------------------
    def callback_call_kill_service(self, future, turtle_name):
        for i, turtle in enumerate(self.alive_turtles_):
            if turtle.name == turtle_name:
                del self.alive_turtles_[i]
                self.publish_alive_turtles()
                self.get_logger().info(f"Killed turtle: {turtle_name}")
                break


def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawnerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
