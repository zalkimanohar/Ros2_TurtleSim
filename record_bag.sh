#!/bin/bash
set -e

cd "$HOME/ros2_ws"
. install/setup.bash

mkdir -p data/raw
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BAG_NAME="data/raw/turtlesim_bag_${TIMESTAMP}"

echo "=== Starting DataOps Bag Recording ==="
echo "Saving to: $BAG_NAME"
echo "Press [Ctrl+C] to stop recording and finalize metadata."

# Run bag recording in the foreground so Ctrl+C gracefully closes it
ros2 bag record -o "$BAG_NAME" /turtle1/pose /turtle1/cmd_vel
