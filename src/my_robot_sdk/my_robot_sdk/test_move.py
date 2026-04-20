import rclpy
from my_robot_sdk.robot_controller import RobotController


def main():
    rclpy.init()

    robot = RobotController()

    executor = rclpy.executors.SingleThreadedExecutor()
    executor.add_node(robot)

    def move2():
        robot.move_to_joint_positions([1.0, 0.5, -0.5, 1.0, 0.2, 0.0])

    def move1():
        robot.move_to_joint_positions(
            [0, 0, 0, 0, 0, 0],
            done_cb=move2
        )

    move1()

    executor.spin()


if __name__ == '__main__':
    main()