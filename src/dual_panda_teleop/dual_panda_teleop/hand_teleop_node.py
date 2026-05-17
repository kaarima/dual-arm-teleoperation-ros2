import cv2
import mediapipe as mp
import numpy as np

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState


class HandTeleop(Node):

    def __init__(self):

        super().__init__(
            "hand_teleop"
        )

        self.pub = self.create_publisher(
            JointState,
            "/joint_states",
            10
        )

        self.cap = None

        self.open_camera()

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6
        )

        self.draw = mp.solutions.drawing_utils

        self.left = np.zeros(7)

        self.right = np.zeros(7)

        self.timer = self.create_timer(
            0.03,
            self.tick
        )

    def open_camera(self):

        if self.cap is not None:
            self.cap.release()

        self.cap = None

        for idx in range(5):

            cap = cv2.VideoCapture(idx)

            ok, _ = cap.read()

            print(f"camera {idx}: {ok}")

            if ok:

                self.cap = cap

                self.get_logger().info(
                    f"USING CAMERA {idx}"
                )

                return

            cap.release()

        self.get_logger().error(
            "NO CAMERA FOUND"
        )

    def map_hand(
        self,
        hand
    ):

        wrist = hand.landmark[0]

        index = hand.landmark[8]

        thumb = hand.landmark[4]

        q = np.zeros(7)

        q[0] = (
            wrist.x - 0.5
        ) * 4.0

        q[1] = (
            wrist.y - 0.5
        ) * 4.0

        q[2] = (
            index.x - wrist.x
        ) * 5.0

        q[3] = (
            index.y - wrist.y
        ) * 5.0

        q[4] = abs(
            thumb.x - index.x
        ) * 6.0

        q[5] = (
            thumb.y - wrist.y
        ) * 4.0

        q[6] = (
            thumb.x - wrist.x
        ) * 4.0

        q = np.clip(
            q,
            -2.5,
            2.5
        )

        return q

    def tick(self):

        if not self.cap.isOpened():

            self.open_camera()

            return

        ok, frame = self.cap.read()

        if not ok:

            self.get_logger().warning(
                "camera reconnect"
            )

            self.open_camera()

            return

        # MIRROR CAMERA
        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        result = self.hands.process(
            rgb
        )

        if result.multi_hand_landmarks:

            for lm, handed in zip(
                result.multi_hand_landmarks,
                result.multi_handedness
            ):

                label = (
                    handed
                    .classification[0]
                    .label
                )

                q = self.map_hand(
                    lm
                )

                if label == "Left":

                    self.left = q

                else:

                    self.right = q

                self.draw.draw_landmarks(
                    frame,
                    lm,
                    self.mp_hands.HAND_CONNECTIONS
                )

        msg = JointState()

        msg.header.stamp = (
            self
            .get_clock()
            .now()
            .to_msg()
        )

        msg.name = [

            "left_panda_joint1",
            "left_panda_joint2",
            "left_panda_joint3",
            "left_panda_joint4",
            "left_panda_joint5",
            "left_panda_joint6",
            "left_panda_joint7",

            "right_panda_joint1",
            "right_panda_joint2",
            "right_panda_joint3",
            "right_panda_joint4",
            "right_panda_joint5",
            "right_panda_joint6",
            "right_panda_joint7"

        ]

        msg.position = (

            list(self.left)

            +

            list(self.right)

        )

        self.pub.publish(
            msg
        )

        cv2.imshow(
            "Hand Teleop",
            frame
        )

        cv2.waitKey(1)

    def destroy_node(self):

        if self.cap:
            self.cap.release()

        cv2.destroyAllWindows()

        super().destroy_node()


def main():

    rclpy.init()

    node = HandTeleop()

    try:

        rclpy.spin(node)

    except KeyboardInterrupt:

        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":

    main()