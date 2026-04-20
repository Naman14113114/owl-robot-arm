import rclpy
from geometry_msgs.msg import PoseStamped
from my_robot_sdk.moveit_interface import MoveItInterface


def main():
    rclpy.init()

    node = MoveItInterface()

    executor = rclpy.executors.SingleThreadedExecutor()
    executor.add_node(node)

    pose = PoseStamped()
    pose.header.frame_id = "base_link"

    pose.pose.position.x = 0.25
    pose.pose.position.y = 0.0
    pose.pose.position.z = 0.25

    pose.pose.orientation.w = 1.0

    node.move_to_pose(pose)

    executor.spin()


if __name__ == "__main__":
    main()