from setuptools import setup

package_name = "dual_panda_teleop"

setup(
    name=package_name,
    version="0.0.0",

    packages=[package_name],

    data_files=[

        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),

        (
            "share/" + package_name,
            ["package.xml"],
        ),
    ],

    install_requires=[
        "setuptools",
    ],

    zip_safe=True,

    maintainer="karima",

    maintainer_email="karima@example.com",

    description="Dual panda teleoperation",

    license="Apache-2.0",

    entry_points={

        "console_scripts": [

            "hand_teleop = dual_panda_teleop.hand_teleop_node:main",

            "moveit_follower = dual_panda_teleop.moveit_follower_node:main",

        ],
    },
)