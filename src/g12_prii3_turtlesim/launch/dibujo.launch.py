from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim'
        ),

        Node(
            package='g12_prii3_turtlesim',
            executable='dibujar_12',
            name='g12_dibujante'
        )
    ])
