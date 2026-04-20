from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    # Packages
    description_pkg = get_package_share_directory(
        'rv5as_so-assy_model_asm_description'
    )

    bringup_pkg = get_package_share_directory(
        'my_robot_bringup'
    )

    # RViz config (YOUR config now)
    rviz_config = os.path.join(
        bringup_pkg,
        'config',
        'simstack.rviz'
    )

    return LaunchDescription([

        # 🔹 Robot description ONLY (no RViz dependency)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    description_pkg,
                    'launch',
                    'display.launch.py'
                )
            ),
            launch_arguments={'use_rviz': 'false'}.items()
        ),

        # 🔹 Your own RViz (clean separation)
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config]
        ),

    ])