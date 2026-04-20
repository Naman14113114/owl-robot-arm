from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os


def generate_launch_description():

    moveit_pkg = get_package_share_directory('rv5as_moveit_config_new')

    ros2_controllers_path = os.path.join(
        moveit_pkg,
        'config',
        'ros2_controllers.yaml'
    )

    control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[
            os.path.join(
                moveit_pkg,
                'config',
                'ros2_controllers.yaml'
            )
        ],
        remappings=[
            ('/controller_manager/robot_description', '/robot_description')
        ],
        output='screen',
    )

    return LaunchDescription([

        # 1. Robot state publisher (URDF + TF)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(moveit_pkg, 'launch', 'rsp.launch.py')
            )
        ),
        control_node,

        # 2. Controllers (ros2_control)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(moveit_pkg, 'launch', 'spawn_controllers.launch.py')
            )
        ),

        # 3. MoveIt core (planning + execution)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(moveit_pkg, 'launch', 'move_group.launch.py')
            )
        ),

        # 4. RViz interface
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(moveit_pkg, 'launch', 'moveit_rviz.launch.py')
            )
        ),

    ])