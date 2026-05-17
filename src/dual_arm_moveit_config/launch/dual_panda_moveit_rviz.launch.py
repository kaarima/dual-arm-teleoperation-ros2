import os

from launch import LaunchDescription

from launch_ros.actions import Node

from launch_ros.parameter_descriptions import ParameterValue

from launch_ros.substitutions import FindPackageShare

from launch.substitutions import Command, PathJoinSubstitution


def generate_launch_description():

    description_package = FindPackageShare(
        "dual_arm_description"
    )

    moveit_package = FindPackageShare(
        "dual_arm_moveit_config"
    )

    robot_description_content = Command(
        [
            "xacro ",
            PathJoinSubstitution(
                [
                    description_package,
                    "urdf",
                    "dual_panda.urdf.xacro",
                ]
            ),
        ]
    )

    robot_description = {
        "robot_description":
        ParameterValue(
            robot_description_content,
            value_type=str,
        )
    }

    robot_description_semantic_content = Command(
        [
            "xacro ",
            PathJoinSubstitution(
                [
                    moveit_package,
                    "config",
                    "dual_panda.srdf.xacro",
                ]
            ),
        ]
    )

    robot_description_semantic = {
        "robot_description_semantic":
        ParameterValue(
            robot_description_semantic_content,
            value_type=str,
        )
    }

    kinematics_yaml = PathJoinSubstitution(
        [
            moveit_package,
            "config",
            "kinematics.yaml",
        ]
    )

    joint_limits_yaml = PathJoinSubstitution(
        [
            moveit_package,
            "config",
            "joint_limits.yaml",
        ]
    )

    moveit_controllers_yaml = PathJoinSubstitution(
        [
            moveit_package,
            "config",
            "moveit_controllers.yaml",
        ]
    )

    robot_state_publisher = Node(

        package="robot_state_publisher",

        executable="robot_state_publisher",

        output="screen",

        parameters=[
            robot_description
        ],
    )

    move_group = Node(

        package="moveit_ros_move_group",

        executable="move_group",

        output="screen",

        parameters=[

            robot_description,

            robot_description_semantic,

            kinematics_yaml,

            joint_limits_yaml,

            moveit_controllers_yaml,

            {
                "planning_pipelines":
                ["ompl"],

                "default_planning_pipeline":
                "ompl",

                "ompl": {
                    "planning_plugin":
                    "ompl_interface/OMPLPlanner"
                },
            },

        ],
    )

    rviz_config = PathJoinSubstitution(
        [
            moveit_package,
            "rviz",
            "dual_panda_moveit.rviz",
        ]
    )

    rviz_env = {

        "LD_LIBRARY_PATH":

        ":".join(

            [

                "/opt/ros/humble/lib",

                "/opt/ros/humble/lib/x86_64-linux-gnu",

                "/opt/ros/humble/opt/rviz_ogre_vendor/lib",

                "/lib/x86_64-linux-gnu",

                "/usr/lib/x86_64-linux-gnu",

            ]
        ),

        "QT_QPA_PLATFORM":

        os.environ.get(
            "QT_QPA_PLATFORM",
            "xcb",
        ),
    }

    rviz = Node(

        package="rviz2",

        executable="rviz2",

        output="screen",

        arguments=[
            "-d",
            rviz_config,
        ],

        parameters=[

            robot_description,

            robot_description_semantic,

        ],

        additional_env=rviz_env,
    )

    return LaunchDescription(
        [

            robot_state_publisher,

            move_group,

            rviz,

        ]
    )