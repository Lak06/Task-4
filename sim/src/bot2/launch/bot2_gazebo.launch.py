from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg_bot1 = FindPackageShare("bot2")
    robot_urdf = PathJoinSubstitution([pkg_bot1, "models", "bot_2.urdf"])

    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": Command([FindExecutable(name="xacro"), " ", robot_urdf])}]
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([FindPackageShare("gazebo_ros"), "launch", "gazebo.launch.py"])
            ])
        ),
        Node(
            package="gazebo_ros",
            executable="spawn_entity.py",
            arguments=["-entity", "bot2", "-file", robot_urdf],
            output="screen"
        )
    ])
