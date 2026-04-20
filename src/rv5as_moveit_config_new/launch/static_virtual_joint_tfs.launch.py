from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_static_virtual_joint_tfs_launch


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("rv5as_so-assy_model_asm", package_name="rv5as_moveit_config_new").to_moveit_configs()
    return generate_static_virtual_joint_tfs_launch(moveit_config)
