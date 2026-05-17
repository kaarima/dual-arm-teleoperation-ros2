# Dual Arm Teleoperation ROS2

## Overview

This project implements a dual-arm teleoperation system using ROS2 Humble, MediaPipe hand tracking, MoveIt, and RViz.

The system captures hand motion from a standard RGB webcam and maps the detected gestures into real-time robot arm motion for a pair of dual Panda robot arms visualized in RViz.

The implementation focuses on:

* Real-time teleoperation
* Dual-arm coordination
* ROS2 integration
* Stable visualization
* Lightweight vision-based interaction

The project was developed as part of the Sereact Teleoperation Challenge.

---

# Features

* ROS2 Humble workspace
* Dual Panda robot arms in RViz
* MoveIt motion planning configuration
* Self-collision-aware robot setup
* MediaPipe hand tracking
* Webcam-based teleoperation
* Dual-arm control
* Gripper-style gesture interaction
* Real-time joint state publishing
* Live TF updates in RViz

---

# System Architecture

```text
RGB Camera
    ↓
MediaPipe Hand Tracking
    ↓
Hand Landmark Extraction
    ↓
Gesture-to-Robot Mapping
    ↓
ROS2 JointState Publishing
    ↓
robot_state_publisher
    ↓
TF Transform Updates
    ↓
RViz Visualization
```

---

# Workspace Structure

```text
sereact_ws/
├── src/
│   ├── dual_arm_description/
│   ├── dual_arm_moveit_config/
│   └── dual_panda_teleop/
├── README.md
└── demo_video.mp4
```

---

# Dependencies

## System Requirements

* Ubuntu 22.04
* ROS2 Humble
* Python 3.10+

## ROS Packages

Install ROS2 and MoveIt dependencies:

```bash
sudo apt update

sudo apt install ros-humble-desktop -y

sudo apt install ros-humble-moveit -y

sudo apt install ros-humble-joint-state-publisher -y

sudo apt install ros-humble-robot-state-publisher -y
```

## Python Dependencies

```bash
pip install mediapipe

pip install opencv-python

pip install numpy
```

---

# Build Instructions

```bash
cd ~/sereact_ws

source /opt/ros/humble/setup.bash

colcon build

source install/setup.bash
```

---

# Running the Project

## Terminal 1 — Launch RViz and MoveIt

```bash
source /opt/ros/humble/setup.bash

source ~/sereact_ws/install/setup.bash

ros2 launch dual_arm_moveit_config dual_panda_moveit_rviz.launch.py
```

## Terminal 2 — Launch Hand Teleoperation

```bash
source /opt/ros/humble/setup.bash

source ~/sereact_ws/install/setup.bash

ros2 run dual_panda_teleop hand_teleop
```

---

# Teleoperation Logic

The system uses MediaPipe Hands to track the operator’s hand landmarks from the webcam stream.

Selected landmarks such as:

* wrist
* thumb tip
* index finger tip

are mapped into robot joint motion.

The left hand controls the left robot arm.
The right hand controls the right robot arm.

Finger distance is additionally used to simulate gripper open/close interaction.

The generated robot joint values are published through ROS2 `JointState` messages and visualized in RViz through TF updates.

---

# Design Choices

The implementation prioritizes:

* responsiveness
* simplicity
* robustness
* low-latency teleoperation

Given the challenge constraints:

* single RGB camera
* no depth sensing
* short implementation timeline

The system uses a lightweight joint-space teleoperation approach instead of a full Cartesian inverse-kinematics teleoperation pipeline.

This architecture can later be extended toward:

* MoveIt Servo
* Cartesian end-effector control
* inverse kinematics
* collision-aware servoing

---

# Known Limitations

* No depth estimation
* Joint-space mapping instead of full Cartesian IK
* Limited gesture vocabulary
* No physical robot hardware integration
* Basic gesture smoothing only

---

# Future Improvements

Potential future work includes:

* Cartesian end-effector teleoperation
* MoveIt Servo integration
* Full inverse kinematics control
* Temporal filtering and smoothing
* Improved gesture recognition
* Bimanual coordination constraints
* Real robot deployment

---

# Demo Video

The demo video is included in the repository:

```text
demo_video.mp4
```

The video demonstrates:

* dual-arm teleoperation
* MediaPipe hand tracking
* real-time RViz motion
* gesture-based interaction

---

# References

## MediaPipe

[https://github.com/google-ai-edge/mediapipe](https://github.com/google-ai-edge/mediapipe)

## MoveIt

[https://moveit.picknik.ai/](https://moveit.picknik.ai/)

## ROS2 Humble

[https://docs.ros.org/en/humble/](https://docs.ros.org/en/humble/)

## Franka Panda

[https://frankaemika.github.io/](https://frankaemika.github.io/)

---

# Author

Karima
