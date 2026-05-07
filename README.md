# ROS 2 Robot Arm Simulation & Control Stack

A modular ROS 2-based robotic arm ecosystem integrating **robot description, Gazebo simulation, MoveIt motion planning, bringup orchestration, and a Python SDK**.

![ROS 2](https://img.shields.io/badge/ROS%202-ready-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![MoveIt](https://img.shields.io/badge/MoveIt-integrated-orange)
![Gazebo](https://img.shields.io/badge/Gazebo-supported-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Overview

This project is organized as a clean robotics pipeline:

1. **Robot Description** defines the mechanical model, geometry, and simulation assets.
2. **MoveIt Config** adds planning, kinematics, joint limits, and controller wiring.
3. **Bringup** launches the full simulation and execution stack.
4. **Python SDK** provides a simple API for scripts and task demos.

<!-- VISUAL 1: full architecture diagram -->
### Architecture at a Glance
![System architecture](docs/assets/robot_stack_architecture.png)

flowchart TD

subgraph group_description["Robot Description"]
  node_desc_pkg["Model package<br/>ROS 2 package"]
  node_desc_urdf["URDF/Xacro<br/>robot model"]
  node_desc_gazebo["Gazebo model<br/>sim config"]
  node_desc_bridge["GZ bridge<br/>bridge config"]
  node_desc_meshes[("Meshes<br/>geometry assets")]
  node_desc_display["Display launch<br/>visualization launch<br/>[display.launch.py]"]
end

subgraph group_planning["MoveIt Config"]
  node_moveit_pkg["MoveIt package<br/>ROS 2 package"]
  node_moveit_urdf["Planning URDF<br/>planning model"]
  node_moveit_srdf["SRDF<br/>planning model"]
  node_moveit_kin["Kinematics<br/>solver config<br/>[kinematics.yaml]"]
  node_moveit_ctrl["Controllers<br/>control config"]
  node_moveit_ros2ctrl["ros2_control<br/>control config"]
  node_moveit_limits["Joint limits<br/>limits config<br/>[joint_limits.yaml]"]
  node_moveit_rviz["MoveIt RViz<br/>visualization config<br/>[moveit.rviz]"]
  node_moveit_launch["MoveIt launch<br/>planning launch"]
  node_moveit_rsp["RSP launch<br/>state pub launch<br/>[rsp.launch.py]"]
end

subgraph group_bringup["Bringup"]
  node_bringup_pkg["Bringup package<br/>ROS 2 package"]
  node_bringup_sim["Simstack launch<br/>orchestration launch"]
  node_bringup_exec["Plan/execute<br/>orchestration launch"]
  node_bringup_rviz["Session RViz<br/>visualization config<br/>[simstack.rviz]"]
end

subgraph group_sdk["Python SDK"]
  node_sdk_pkg["SDK package<br/>Python package"]
  node_sdk_iface["MoveIt API<br/>python module"]
  node_sdk_ctrl["Robot ctrl<br/>python module"]
  node_sdk_demo["Task demo<br/>script<br/>[task_demo.py]"]
end

node_desc_pkg -->|"defines"| node_desc_urdf
node_desc_pkg -->|"includes"| node_desc_meshes
node_desc_pkg -->|"supports"| node_desc_gazebo
node_desc_pkg -->|"bridges"| node_desc_bridge
node_desc_pkg -->|"visualizes"| node_desc_display
node_moveit_pkg -->|"adapts"| node_moveit_urdf
node_moveit_pkg -->|"semantics"| node_moveit_srdf
node_moveit_pkg -->|"solves"| node_moveit_kin
node_moveit_pkg -->|"constrains"| node_moveit_limits
node_moveit_pkg -->|"routes"| node_moveit_ctrl
node_moveit_pkg -->|"executes"| node_moveit_ros2ctrl
node_moveit_pkg -->|"visualizes"| node_moveit_rviz
node_moveit_pkg -->|"starts"| node_moveit_launch
node_moveit_pkg -->|"publishes"| node_moveit_rsp
node_bringup_pkg -->|"orchestrates"| node_bringup_sim
node_bringup_pkg -->|"orchestrates"| node_bringup_exec
node_bringup_pkg -->|"configures"| node_bringup_rviz
node_bringup_sim -->|"loads"| node_desc_urdf
node_bringup_sim -->|"starts"| node_moveit_launch
node_bringup_sim -->|"starts"| node_moveit_rsp
node_bringup_sim -->|"starts"| node_moveit_ros2ctrl
node_bringup_exec -->|"invokes"| node_sdk_iface
node_sdk_pkg -->|"exposes"| node_sdk_iface
node_sdk_pkg -->|"wraps"| node_sdk_ctrl
node_sdk_pkg -->|"demonstrates"| node_sdk_demo
node_sdk_ctrl -->|"uses"| node_sdk_iface
node_sdk_iface -->|"targets"| node_moveit_launch
node_moveit_ctrl -->|"handoff"| node_moveit_ros2ctrl
node_moveit_urdf -->|"derives from"| node_desc_urdf
node_moveit_rviz -->|"observes"| node_moveit_launch
node_desc_display -.->|"reuses"| node_bringup_rviz

click node_desc_pkg "https://github.com/naman14113114/owl-robot-arm/tree/main/src/rv5as_so-assy_model_asm_description-20260413T091140Z-3-001/rv5as_so-assy_model_asm_description"
click node_desc_urdf "https://github.com/naman14113114/owl-robot-arm/blob/main/src/rv5as_so-assy_model_asm_description-20260413T091140Z-3-001/rv5as_so-assy_model_asm_description/urdf/rv5as_so-assy_model_asm.xacro"
click node_desc_gazebo "https://github.com/naman14113114/owl-robot-arm/blob/main/src/rv5as_so-assy_model_asm_description-20260413T091140Z-3-001/rv5as_so-assy_model_asm_description/urdf/rv5as_so-assy_model_asm.gazebo"
click node_desc_bridge "https://github.com/naman14113114/owl-robot-arm/blob/main/src/rv5as_so-assy_model_asm_description-20260413T091140Z-3-001/rv5as_so-assy_model_asm_description/config/ros_gz_bridge_gazebo.yaml"
click node_desc_meshes "https://github.com/naman14113114/owl-robot-arm/tree/main/src/rv5as_so-assy_model_asm_description-20260413T091140Z-3-001/rv5as_so-assy_model_asm_description/meshes"
click node_desc_display "https://github.com/naman14113114/owl-robot-arm/blob/main/src/rv5as_so-assy_model_asm_description-20260413T091140Z-3-001/rv5as_so-assy_model_asm_description/launch/display.launch.py"
click node_moveit_pkg "https://github.com/naman14113114/owl-robot-arm/tree/main/src/rv5as_moveit_config_new"
click node_moveit_urdf "https://github.com/naman14113114/owl-robot-arm/blob/main/src/rv5as_moveit_config_new/config/rv5as_so-assy_model_asm.urdf.xacro"
click node_moveit_srdf "https://github.com/naman14113114/owl-robot-arm/blob/main/src/rv5as_moveit_config_new/config/rv5as_so-assy_model_asm.srdf"
click node_moveit_kin "https://github.com/naman14113114/owl-robot-arm/blob/main/src/rv5as_moveit_config_new/config/kinematics.yaml"
click node_moveit_ctrl "https://github.com/naman14113114/owl-robot-arm/blob/main/src/rv5as_moveit_config_new/config/moveit_controllers.yaml"
click node_moveit_ros2ctrl "https://github.com/naman14113114/owl-robot-arm/blob/main/src/rv5as_moveit_config_new/config/ros2_controllers.yaml"
click node_moveit_limits "https://github.com/naman14113114/owl-robot-arm/blob/main/src/rv5as_moveit_config_new/config/joint_limits.yaml"
click node_moveit_rviz "https://github.com/naman14113114/owl-robot-arm/blob/main/src/rv5as_moveit_config_new/config/moveit.rviz"
click node_moveit_launch "https://github.com/naman14113114/owl-robot-arm/blob/main/src/rv5as_moveit_config_new/launch/move_group.launch.py"
click node_moveit_rsp "https://github.com/naman14113114/owl-robot-arm/blob/main/src/rv5as_moveit_config_new/launch/rsp.launch.py"
click node_bringup_pkg "https://github.com/naman14113114/owl-robot-arm/tree/main/src/my_robot_bringup"
click node_bringup_sim "https://github.com/naman14113114/owl-robot-arm/blob/main/src/my_robot_bringup/launch/simstack_bringup.launch.py"
click node_bringup_exec "https://github.com/naman14113114/owl-robot-arm/blob/main/src/my_robot_bringup/launch/plan_execute.launch.py"
click node_bringup_rviz "https://github.com/naman14113114/owl-robot-arm/blob/main/src/my_robot_bringup/config/simstack.rviz"
click node_sdk_pkg "https://github.com/naman14113114/owl-robot-arm/tree/main/src/my_robot_sdk/my_robot_sdk"
click node_sdk_iface "https://github.com/naman14113114/owl-robot-arm/blob/main/src/my_robot_sdk/my_robot_sdk/moveit_interface.py"
click node_sdk_ctrl "https://github.com/naman14113114/owl-robot-arm/blob/main/src/my_robot_sdk/my_robot_sdk/robot_controller.py"
click node_sdk_demo "https://github.com/naman14113114/owl-robot-arm/blob/main/src/my_robot_sdk/my_robot_sdk/task_demo.py"

classDef toneNeutral fill:#f8fafc,stroke:#334155,stroke-width:1.5px,color:#0f172a
classDef toneBlue fill:#dbeafe,stroke:#2563eb,stroke-width:1.5px,color:#172554
classDef toneAmber fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#78350f
classDef toneMint fill:#dcfce7,stroke:#16a34a,stroke-width:1.5px,color:#14532d
classDef toneRose fill:#ffe4e6,stroke:#e11d48,stroke-width:1.5px,color:#881337
classDef toneIndigo fill:#e0e7ff,stroke:#4f46e5,stroke-width:1.5px,color:#312e81
classDef toneTeal fill:#ccfbf1,stroke:#0f766e,stroke-width:1.5px,color:#134e4a
class node_desc_pkg,node_desc_urdf,node_desc_gazebo,node_desc_bridge,node_desc_meshes,node_desc_display toneBlue
class node_moveit_pkg,node_moveit_urdf,node_moveit_srdf,node_moveit_kin,node_moveit_ctrl,node_moveit_ros2ctrl,node_moveit_limits,node_moveit_rviz,node_moveit_launch,node_moveit_rsp toneAmber
class node_bringup_pkg,node_bringup_sim,node_bringup_exec,node_bringup_rviz toneMint
class node_sdk_pkg,node_sdk_iface,node_sdk_ctrl,node_sdk_demo toneRose

---

## What This Project Contains

### Robot Description
- URDF/Xacro robot model
- Meshes and geometry assets
- Gazebo simulation config
- ROS ↔ Gazebo bridge config
- Visualization launch file

<!-- VISUAL 2: RViz robot model screenshot -->
#### Insert here
**Needed:** clean RViz screenshot of the robot loaded from the description package.  
**Best caption:** *Robot model rendered from the description package.*

---

### MoveIt Configuration
- Planning URDF
- SRDF semantics
- Kinematics solver config
- Joint limits
- MoveIt controllers
- ros2_control config
- RViz planning config
- MoveIt launch files

<!-- VISUAL 3: MoveIt planning scene screenshot -->
#### Insert here
**Needed:** screenshot of MoveIt running in RViz with planning scene visible.  
**Best caption:** *MoveIt planning scene and motion goal execution.*

---

### Bringup Package
- Full simulation launch
- Plan-and-execute launch
- Session RViz config

<!-- VISUAL 4: terminal + RViz + Gazebo combo -->
#### Insert here
**Needed:** one wide screenshot showing terminal logs, Gazebo, and RViz together.  
**Best caption:** *End-to-end system bringup in one session.*

---

### Python SDK
- MoveIt API wrapper
- Robot controller wrapper
- Task demo script

<!-- VISUAL 5: terminal output or script demo -->
#### Insert here
**Needed:** terminal screenshot or code snippet showing a Python command controlling the robot.  
**Best caption:** *Python SDK driving motion commands.*

---

## Repository Layout

```text
src/
├── rv5as_so-assy_model_asm_description/
│   ├── urdf/
│   ├── meshes/
│   ├── config/
│   └── launch/
├── rv5as_moveit_config_new/
│   ├── config/
│   └── launch/
├── my_robot_bringup/
│   ├── launch/
│   └── config/
└── my_robot_sdk/
    └── my_robot_sdk/
```

---

## How the Stack Connects

The packages are intentionally separated so each layer can be tested independently before the full integration.

Your provided architecture shows how the model package feeds the MoveIt config, how bringup orchestrates the runtime, and how the SDK talks to the planning/execution layer. fileciteturn0file0

<!-- VISUAL 6: simplified flow diagram -->
### Insert here
**Needed:** a simplified horizontal flow graphic: `SDK → Bringup → MoveIt → Controllers → Robot`.  
*Command flow from Python to physical or simulated motion.*

---

## Getting Started

```bash
colcon build
source install/setup.bash
```

### Launch Simulation
```bash
ros2 launch my_robot_bringup simstack_bringup.launch.py
```

### Run the Demo
```bash
ros2 run my_robot_sdk task_demo.py
```

---

## Recommended Screenshots and Media

Use these assets to make the README feel complete:

- **Top banner image** — a wide hero shot or rendered robot image
- **Architecture diagram** — the package flow visual
- **RViz screenshot** — planning scene and robot state
- **Gazebo screenshot** — the simulated robot in motion
- **Execution GIF** — moving from pose A to pose B
- **Terminal strip** — launch logs and success output

<!-- VISUAL 7: demo GIF -->
#### Insert here
**Needed:** short GIF of the robot executing a planned motion.  
**Best caption:** *Motion demo from a scripted task.*

---

## Suggested Animated Demo Ideas

- A short GIF showing **launch → plan → execute**
- A split-screen clip of **RViz planning on one side and Gazebo motion on the other**
- A looped GIF of the robot returning to a **home pose**
- A before/after comparison of **planning goal set vs. trajectory executed**

---

## Design Notes

- Keep the README visually spaced out.
- Use one strong diagram near the top.
- Add screenshots only where they explain the layer being described.
- Keep code blocks short and practical.
- Prefer captions over long paragraphs under images.

---

## Contributing

Pull requests and improvements are welcome. The project is structured so each subsystem can be extended independently.

---

## License

Add your chosen license here.
