import time
import math

import rclpy

from rclpy.node import Node
from geometry_msgs.msg import PoseArray

from moveit_msgs.action import MoveGroup

from rclpy.action import ActionClient


class MoveFollower(Node):

    def __init__(self):

        super().__init__("moveit_follower")

        self.client = ActionClient(
            self,
            MoveGroup,
            "/move_action"
        )

        self.last_exec = 0.0

        self.min_period = 1.0   # 1 Hz ONLY

        self.last_left = None
        self.last_right = None

        self.deadband = 0.03

        self.subscription = self.create_subscription(
            PoseArray,
            "/dual_arm/target_pose",
            self.callback,
            10
        )

        self.get_logger().info(
            "Move follower throttled"
        )

    def moved(self, p, old):

        if old is None:
            return True

        dx = p.position.x - old.position.x
        dy = p.position.y - old.position.y

        return math.sqrt(
            dx*dx + dy*dy
        ) > self.deadband

    def callback(self, msg):

        now = time.time()

        if now - self.last_exec < self.min_period:
            return

        if len(msg.poses) < 2:
            return

        left = msg.poses[0]
        right = msg.poses[1]

        left_move = self.moved(
            left,
            self.last_left
        )

        right_move = self.moved(
            right,
            self.last_right
        )

        if not left_move and not right_move:
            return

        self.last_left = left
        self.last_right = right

        self.last_exec = now

        self.get_logger().info(
            "motion update"
        )


def main():

    rclpy.init()

    node = MoveFollower()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()