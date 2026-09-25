#!/bin/bash

# Exit immediately if any critical setup command fails
set -e

# Ensure we are operating inside the workspace root
WORKSPACE_DIR="$HOME/ros2_ws"
cd "$WORKSPACE_DIR"

echo "=========================================="
echo "Step 1: Building workspace..."
echo "=========================================="
colcon build --symlink-install

echo "=========================================="
echo "Step 2: Sourcing environment..."
echo "=========================================="
source install/setup.bash

echo "=========================================="
echo "Step 3: Setting up DataOps directories..."
echo "=========================================="
mkdir -p data/raw data/logs

# Generate unique timestamps for logs and bag files
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="data/logs/run_${TIMESTAMP}.log"
BAG_NAME="data/raw/turtlesim_bag_${TIMESTAMP}"

echo "=========================================="
echo "Step 4: Launching ROS 2 system in background..."
echo "=========================================="
# Launch your specific configuration with log collection
ros2 launch my_robot_bringup turtlesim_catch_them_all.launch.xml > "$LOG_FILE" 2>&1 &
LAUNCH_PID=$!
echo "-> Launch process running with PID: $LAUNCH_PID"
echo "-> Output redirected to: $LOG_FILE"

# Give the nodes 3 seconds to fully initialize
sleep 3

echo "=========================================="
echo "Step 5: Starting ros2 bag recording..."
echo "=========================================="
# Recording relevant telemetry topics
ros2 bag record -o "$BAG_NAME" /turtle1/pose /turtle1/cmd_vel &
BAG_PID=$!
echo "-> Bag recording running with PID: $BAG_PID"
echo "-> Saving data to: $BAG_NAME"

echo "=========================================="
echo "Pipeline Active! Press [Ctrl+C] to stop."
echo "=========================================="

# Trap Ctrl+C (SIGINT) to ensure background processes are killed gracefully
trap "echo -e '\nStopping background processes...'; kill $LAUNCH_PID $BAG_PID 2>/dev/null; wait; echo 'Pipeline shut down successfully.'; exit 0" SIGINT

# Keep the script running to monitor background jobs
wait
