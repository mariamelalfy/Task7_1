from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node


def generate_launch_description():

    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim'
    )

    controller_node = ExecuteProcess(
        cmd=[
            'gnome-terminal',
            '--',
            'bash',
            '-c',
            'source /opt/ros/$ROS_DISTRO/setup.bash && '
            'source ~/ros2_ws/install/setup.bash && '
            'ros2 run task_7_1 controller '
            '--ros-args -r /cmd_vel:=/turtle1/cmd_vel; '
            'exec bash'
        ],
        output='screen'
    )

    return LaunchDescription([
        turtlesim_node,
        controller_node
    ])
