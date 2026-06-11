import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # Paths
    bringup_dir = get_package_share_directory('warehouse_amr_bringup')
    description_dir = get_package_share_directory('warehouse_amr_description')
    workspace_dir = os.path.abspath(os.path.join(bringup_dir, '../../../..'))
    world_file = os.path.join(workspace_dir, 'worlds', 'warehouse.sdf')
    bridge_config = os.path.join(workspace_dir, 'config', 'bridge.yaml')
    
    # Parse Xacro
    xacro_file = os.path.join(description_dir, 'urdf', 'amr.urdf.xacro')
    doc = xacro.process_file(xacro_file)
    robot_description = {'robot_description': doc.toxml(), 'use_sim_time': True}

    # Nodes
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[robot_description]
    )

    # NEW: Joint State Publisher handles continuous wheel joints
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        parameters=[robot_description]
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': f'-r {world_file}'}.items()
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-world', 'warehouse', '-string', doc.toxml(), '-name', 'warehouse_amr', '-z', '0.3'],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': bridge_config, 'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher,  # Added to launch sequence
        gazebo,
        spawn_robot,
        bridge
    ])
