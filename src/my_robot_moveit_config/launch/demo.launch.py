import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro

def generate_launch_description():
    # Parse URDF/Xacro
    desc_path = get_package_share_directory('my_robot_description')
    xacro_file = os.path.join(desc_path, 'urdf', 'my_robot.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_description = {'robot_description': robot_description_config.toxml()}

    # Parse SRDF
    config_path = get_package_share_directory('my_robot_moveit_config')
    srdf_file = os.path.join(config_path, 'config', 'my_robot.srdf')
    with open(srdf_file, 'r') as f:
        robot_description_semantic = {'robot_description_semantic': f.read()}

    # Kinematics & Joint limits
    kinematics_yaml = os.path.join(config_path, 'config', 'kinematics.yaml')
    joint_limits_yaml = os.path.join(config_path, 'config', 'joint_limits.yaml')
    ompl_yaml = os.path.join(config_path, 'config', 'ompl_planning.yaml')

    # 1. Robot State Publisher (Publishes transforms /tf)
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # 2. MoveGroup Node
    move_group_node = Node(
        package='moveit_ros_move_group',
        executable='move_group',
        output='screen',
        parameters=[
            robot_description,
            robot_description_semantic,
            kinematics_yaml,
            joint_limits_yaml,
            ompl_yaml,
            {'use_sim_time': False}
        ]
    )

    # 3. RViz with MoveIt plugin
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        parameters=[
            robot_description,
            robot_description_semantic,
            kinematics_yaml,
        ]
    )

    return LaunchDescription([
        robot_state_publisher_node,
        move_group_node,
        rviz_node
    ])
