#!/bin/bash
set -e

cd "$HOME/ros2_ws"

echo "=== Building & Sourcing Workspace ==="
colcon build --symlink-install
. install/setup.bash

echo "=== Setting up Logs Directory ==="
mkdir -p data/logs
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="data/logs/run_${TIMESTAMP}.log"

echo "=== Launching ROS 2 System (Logs -> $LOG_FILE) ==="
# Optional: If you want background log collection + visible console output
ros2 launch my_robot_bringup turtlesim_catch_them_all.launch.xml 2>&1 | tee "$LOG_FILE"
