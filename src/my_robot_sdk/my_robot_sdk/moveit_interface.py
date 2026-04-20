import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import MotionPlanRequest, Constraints, PositionConstraint
from geometry_msgs.msg import PoseStamped
from shape_msgs.msg import SolidPrimitive


class MoveItInterface(Node):

    def __init__(self):
        super().__init__('moveit_interface')

        self.client = ActionClient(
            self,
            MoveGroup,
            '/move_action'
        )

        self.group_name = "arm"
        self.done_cb = None

    def move_to_pose(self, pose: PoseStamped, done_cb=None):
        self.done_cb = done_cb

        if not self.client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error("MoveIt action server not available")
            return

        goal = MoveGroup.Goal()

        # -------------------------------
        # CLEAN planning request
        # -------------------------------
        req = MotionPlanRequest()
        req.group_name = self.group_name

        # ---- POSITION constraint ONLY (no orientation for now)
        constraints = Constraints()

        pos_constraint = PositionConstraint()
        pos_constraint.header = pose.header
        pos_constraint.link_name = "RV5AS_J6_INTERFACE_1"  # your end-effector

        # Define a small region (NOT exact point)
        box = SolidPrimitive()
        box.type = SolidPrimitive.BOX
        box.dimensions = [0.01, 0.01, 0.01]  # 1cm tolerance

        pos_constraint.constraint_region.primitives.append(box)
        pos_constraint.constraint_region.primitive_poses.append(pose.pose)

        pos_constraint.weight = 1.0

        constraints.position_constraints.append(pos_constraint)

        req.goal_constraints.append(constraints)

        # Important defaults
        req.num_planning_attempts = 5
        req.allowed_planning_time = 2.0

        goal.request = req

        # -------------------------------
        self.get_logger().info("Sending MoveIt goal...")
        future = self.client.send_goal_async(goal)
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error("MoveIt goal rejected")
            return

        self.get_logger().info("MoveIt goal accepted")

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        self.get_logger().info("MoveIt execution completed")

        if self.done_cb:
            cb = self.done_cb
            self.done_cb = None
            cb()
        else:
            rclpy.shutdown()