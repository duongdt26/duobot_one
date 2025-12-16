# Vid 2 SECOND STEP
import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction # Vid 2 ROS2_control: TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch.substitutions import Command # Vid 2 ROS2_control
from launch.actions import RegisterEventHandler # Vid 2 ROS2_control
from launch.event_handlers import OnProcessStart # Vid 2 ROS2_control

from launch_ros.actions import Node

def generate_launch_description():

    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    # package_name='articubot_one' #<--- CHANGE ME
    package_name='duobot_one' #<--- CHANGE ME
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'false', 'use_ros2_control': 'true'}.items()
    )

    

    # # Include the Gazebo launch file, provided by the gazebo_ros package
    # gazebo = IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(
    #                 get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    #          )

    # # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    # spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
    #                     arguments=['-topic', 'robot_description',
    #                                '-entity', 'my_bot'],
    #                     output='screen')


    # Vid 2 ROS2_control
    # gazebo_params_file = os.path.join(get_package_share_directory(package_name),'config','gazebo_params.yaml')  #

    # Vid 2 ROS2_control
    # Lenh nay yeu cau node robot state publisher tra ve tham so mo ta robot cua no duoi dang chuoi(string)
    robot_description = Command(['ros2 param get --hide-type /robot_state_publisher robot_description'])
    controller_params_file = os.path.join(get_package_share_directory(package_name),'config','my_controllers.yaml')

    # Vid 2 ROS2_control
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[{'robot_description': robot_description},
                    controller_params_file], # bat cu thu gi trong bien robot_decription 
    )

    delayed_controller_manager = TimerAction(period=3.0, actions=[controller_manager])

    # Vid 1 ROS2_control
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    # Vid 2 ROS2_control
    delayed_diff_drive_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[diff_drive_spawner],
        )
    )

    # Vid 1 ROS2_control
    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    # Vid 2 ROS2_control
    delayed_joint_broad_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[joint_broad_spawner],
        )
    )

    # Launch them all!
    return LaunchDescription([
        rsp,
        # gazebo,
        # spawn_entity,
        # Vid 1 ROS2_control
        delayed_controller_manager,
        delayed_diff_drive_spawner,
        delayed_joint_broad_spawner,
        # Vid 1 ROS2_control
    ])