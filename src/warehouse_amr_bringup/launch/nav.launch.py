import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    bringup_dir = get_package_share_directory('warehouse_amr_bringup')
    workspace_dir = os.path.abspath(os.path.join(bringup_dir, '../../../..'))
    map_file = os.path.join(workspace_dir, 'maps', 'warehouse_map.yaml')

    nav2_launch_file = os.path.join(
        get_package_share_directory('nav2_bringup'), 'launch', 'bringup_launch.py')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(nav2_launch_file),
            launch_arguments={
                'map': map_file,
                'use_sim_time': 'true'
            }.items()
        )
    ])
