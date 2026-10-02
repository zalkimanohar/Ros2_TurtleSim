#!/bin/bash
set -e

WORKSPACE_DIR="$HOME/ros2_ws"
cd "$WORKSPACE_DIR"

echo "=========================================="
echo "Step 1: Building workspace..."
echo "=========================================="
colcon build --symlink-install

echo "=========================================="
echo "Step 2: Sourcing environment..."
echo "=========================================="
#source install/setup.bash

echo "=========================================="
echo "Step 3: Setting up DataOps directories..."
echo "=========================================="
mkdir -p data/raw data/logs

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BAG_NAME="data/raw/turtlesim_bag_${TIMESTAMP}"

echo "=========================================="
echo "Step 4: Starting ros2 bag recording in background..."
echo "=========================================="
# Record telemetry quietly in the background
ros2 bag record -o "$BAG_NAME" /turtle1/pose /turtle1/cmd_vel > /dev/null 2>&1 &
BAG_PID=$!
echo "-> Bag recording started (PID: $BAG_PID)"
echo "-> Saving to: $BAG_NAME"

echo "=========================================="
echo "Step 5: Launching ROS 2 system (Foreground)..."
echo "=========================================="
echo "-> Press [Ctrl+C] to stop everything when done."

# Trap Ctrl+C to clean up the background bag recorder when you exit the launch
trap "echo -e '\nStopping bag recorder...'; kill $BAG_PID 2>/dev/null; wait; exit 0" SIGINT

# Run launch in the FOREGROUND so it behaves identically to manual execution
ros2 launch my_robot_bringup turtlesim_catch_them_all.launch.xml
