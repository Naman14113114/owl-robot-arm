import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint


class RobotController(Node):

    def __init__(self):
        super().__init__('robot_controller')

        self.client = ActionClient(
            self,
            FollowJointTrajectory,
            '/arm_controller/follow_joint_trajectory'
        )

        self.joint_names = [
            'Revolute_1',
            'Revolute_2',
            'Revolute_3',
            'Revolute_4',
            'Revolute_5',
            'Revolute_6'
        ]

    def move_to_joint_positions(self, positions, done_cb=None):

        self.done_cb = done_cb

        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory.joint_names = self.joint_names

        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start.sec = 3

        goal_msg.trajectory.points.append(point)

        self.get_logger().info('Checking controller...')

        if not self.client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('Controller NOT available!')
            return

        self.get_logger().info('Controller connected')

        self.get_logger().info('Sending goal...')
        send_goal_future = self.client.send_goal_async(goal_msg)

        def goal_response_callback(future):
            goal_handle = future.result()

            if not goal_handle.accepted:
                self.get_logger().error('Goal rejected')
                return

            self.get_logger().info('Goal accepted')

            result_future = goal_handle.get_result_async()
            result_future.add_done_callback(self.result_callback)

        send_goal_future.add_done_callback(goal_response_callback)

    def result_callback(self, future):
        self.get_logger().info('Motion completed')

        if hasattr(self, 'done_cb') and self.done_cb is not None:
            cb = self.done_cb
            self.done_cb = None  # prevent reuse
            cb()
        else:
            rclpy.shutdown()