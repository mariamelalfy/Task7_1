# Task 7.1 - First Robot Control

ROS 2 package implementing keyboard-controlled turtle movement and
color perception using turtlesim.

## Features

- W/A/S/D keyboard control
- Non-holonomic turtle movement
- `/cmd_vel` Twist publisher
- `/turtle1/color_sensor` subscriber
- Dominant color detection
- `/dominant_color` publisher
- ROS 2 parameters for topic names
- Launch file for turtlesim and controller

## Run

```bash
cd ~/ros2_ws
source /opt/ros/$ROS_DISTRO/setup.bash
source install/setup.bash
ros2 launch task_7_1 turtle_controller.launch.py
