import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Package and URDF paths
    pkg_name = "my_robot_description"
    pkg_dir = get_package_share_directory(pkg_name)
    bot1 = os.path.join(pkg_dir, "urdf", "rob1.urdf")
    bot2= os.path.join(pkg_dir, "urdf", "rob2.urdf")

    # Load both URDF files
    with open(bot1, 'r') as infp:
        robot1_description = infp.read()
    with open(bot2, 'r') as infp:
        robot2_description = infp.read()

    # Launch Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("gazebo_ros"), "launch", "gazebo.launch.py")
        )
    )

    # Robot 1
    robot1_spawn = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-entity", "robot1",
            "-file", bot1,
            "-robot_namespace", "/robot1",
            "-x", "0", "-y", "0", "-z", "0.1"
        ],
        output="screen",
    )

    robot1_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        namespace="robot1",
        output="screen",
        parameters=[{"robot_description": robot1_description}],
    )

    # Robot 2
    robot2_spawn = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-entity", "robot2",
            "-file", bot2,
            "-robot_namespace", "/robot2",
            "-x", "2", "-y", "0", "-z", "0.1"
        ],
        output="screen",
    )

    robot2_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        namespace="robot2",
        output="screen",
        parameters=[{"robot_description": robot2_description}],
    )

    return LaunchDescription([
        gazebo,
        robot1_state_publisher,
        robot1_spawn,
        robot2_state_publisher,
        robot2_spawn,
    ])
