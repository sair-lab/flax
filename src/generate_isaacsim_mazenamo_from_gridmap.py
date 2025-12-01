import os
os.environ["OMNI_KIT_ACCEPT_EULA"] = "YES"

import math
import random
import pickle as pkl

from isaacsim import SimulationApp
from my_utils import *
from my_utils.pddl_utils import *

# Create the SimulationApp instance
simulation_app = SimulationApp(launch_config=config["launch_config"])

# Late import, must be done after SimulationApp is created
from isaacsim.core.utils import prims
from isaacsim.core.utils.rotations import euler_angles_to_quat
from isaacsim.core.utils.stage import save_stage, open_stage, get_current_stage
from isaacsim.core.prims import SingleRigidPrim
from pxr import UsdPhysics
from my_utils.isaacsim_utils import *


if __name__ == "__main__":
    # Open the given environment in a new stage
    print(f"Loading Stage {config['env_url']}")
    if not open_stage(config["env_url"]):
        print(f"Could not open stage: {config['env_url']}, closing application..")
        simulation_app.close()

    # Clear any previous semantic data in the loaded stage
    if config["clear_previous_semantics"]:
        stage = get_current_stage()
        remove_previous_semantics(stage)

    problem_size = 10
    problem_mode = "hard"
    problem_idx = 19

    problem_map_dir = f"pddl_files/problems/mazenamo_problems/map_{problem_size}x{problem_size}_{problem_mode}"
    problem_map_file = f"{problem_map_dir}/mazenamo_map_{problem_idx}.pkl"
    with open(problem_map_file, "rb") as f:
        problem_dict = pkl.load(f)

    grid = problem_dict["grid"]
    robot_pos = problem_dict["robot_pos"]
    robot_direction = problem_dict["robot_direction"]

    # Build outer walls
    num_rack_long = (problem_size - 1) // 3
    num_cone = (problem_size - 1) % 3
    rack_long_idx = 0
    cone_idx = 0
    light_idx = 0
    heavy_idx = 0

    for i in range(num_rack_long):
        # up wall
        prims.create_prim(
            prim_path=f"/World/RackLongEmpty_{rack_long_idx}",
            position=(
                (-problem_size / 2 + 1.5 + i * 3) * UNIT_SIZE,
                (problem_size / 2 - 0.5) * UNIT_SIZE,
                0
            ),
            orientation=euler_angles_to_quat([0, 0, math.pi/2]),
            scale=(0.01, 0.01, 0.01),
            usd_path=config["rack_long_empty"]["url"],
            semantic_label=config["rack_long_empty"]["class"],
        )
        # prim = SingleRigidPrim(
        #     prim_path=f"/World/RackLongEmpty_{rack_long_idx}",
        #     name=f"RackLongEmpty_{rack_long_idx}",
        #     mass=500.0,
        # )
        # UsdPhysics.CollisionAPI.Apply(prim.prim)
        rack_long_idx += 1
        # down wall
        prims.create_prim(
            prim_path=f"/World/RackLongEmpty_{rack_long_idx}",
            position=(
                (problem_size / 2 - 1.5 - i * 3) * UNIT_SIZE,
                (-problem_size / 2 + 0.5) * UNIT_SIZE,
                0
            ),
            orientation=euler_angles_to_quat([0, 0, math.pi/2]),
            scale=(0.01, 0.01, 0.01),
            usd_path=config["rack_long_empty"]["url"],
            semantic_label=config["rack_long_empty"]["class"],
        )
        # prim = SingleRigidPrim(
        #     prim_path=f"/World/RackLongEmpty_{rack_long_idx}",
        #     name=f"RackLongEmpty_{rack_long_idx}",
        #     mass=500.0,
        # )
        # UsdPhysics.CollisionAPI.Apply(prim.prim)
        rack_long_idx += 1
        # left wall
        prims.create_prim(
            prim_path=f"/World/RackLongEmpty_{rack_long_idx}",
            position=(
                (-problem_size / 2 + 0.5) * UNIT_SIZE,
                (-problem_size / 2 + 1.5 + i * 3) * UNIT_SIZE,
                0
            ),
            orientation=euler_angles_to_quat([0, 0, 0]),
            scale=(0.01, 0.01, 0.01),
            usd_path=config["rack_long_empty"]["url"],
            semantic_label=config["rack_long_empty"]["class"],
        )
        # prim = SingleRigidPrim(
        #     prim_path=f"/World/RackLongEmpty_{rack_long_idx}",
        #     name=f"RackLongEmpty_{rack_long_idx}",
        #     mass=500.0,
        # )
        # UsdPhysics.CollisionAPI.Apply(prim.prim)
        rack_long_idx += 1
        # right wall
        prims.create_prim(
            prim_path=f"/World/RackLongEmpty_{rack_long_idx}",
            position=(
                (problem_size / 2 - 0.5) * UNIT_SIZE,
                (problem_size / 2 - 1.5 - i * 3) * UNIT_SIZE,
                0
            ),
            orientation=euler_angles_to_quat([0, 0, 0]),
            scale=(0.01, 0.01, 0.01),
            usd_path=config["rack_long_empty"]["url"],
            semantic_label=config["rack_long_empty"]["class"],
        )
        # prim = SingleRigidPrim(
        #     prim_path=f"/World/RackLongEmpty_{rack_long_idx}",
        #     name=f"RackLongEmpty_{rack_long_idx}",
        #     mass=500.0,
        # )
        # UsdPhysics.CollisionAPI.Apply(prim.prim)
        rack_long_idx += 1

    for i in range(num_cone):
        # up wall
        prims.create_prim(
            prim_path=f"/World/TrafficCone_{cone_idx}",
            position=(
                (-problem_size / 2 + num_rack_long * 3 + 0.5 + i) * UNIT_SIZE,
                (problem_size / 2 - 0.5) * UNIT_SIZE,
                0
            ),
            orientation=euler_angles_to_quat([0, 0, 0]),
            scale=(0.01, 0.01, 0.01),
            usd_path=config["traffic_cone"]["url"],
            semantic_label=config["traffic_cone"]["class"],
        )
        prim = SingleRigidPrim(
            prim_path=f"/World/TrafficCone_{cone_idx}",
            name=f"TrafficCone_{cone_idx}",
            mass=500.0,
        )
        UsdPhysics.CollisionAPI.Apply(prim.prim)
        cone_idx += 1
        # down wall
        prims.create_prim(
            prim_path=f"/World/TrafficCone_{cone_idx}",
            position=(
                (problem_size / 2 - num_rack_long * 3 - 0.5 - i) * UNIT_SIZE,
                (-problem_size / 2 + 0.5) * UNIT_SIZE,
                0
            ),
            orientation=euler_angles_to_quat([0, 0, 0]),
            scale=(0.01, 0.01, 0.01),
            usd_path=config["traffic_cone"]["url"],
            semantic_label=config["traffic_cone"]["class"],
        )
        prim = SingleRigidPrim(
            prim_path=f"/World/TrafficCone_{cone_idx}",
            name=f"TrafficCone_{cone_idx}",
            mass=500.0,
        )
        UsdPhysics.CollisionAPI.Apply(prim.prim)
        cone_idx += 1
        # left wall
        prims.create_prim(
            prim_path=f"/World/TrafficCone_{cone_idx}",
            position=(
                (-problem_size / 2 + 0.5) * UNIT_SIZE,
                (-problem_size / 2 + num_rack_long * 3 + 0.5 + i) * UNIT_SIZE,
                0
            ),
            orientation=euler_angles_to_quat([0, 0, 0]),
            scale=(0.02, 0.02, 0.02),
            usd_path=config["traffic_cone"]["url"],
            semantic_label=config["traffic_cone"]["class"],
        )
        prim = SingleRigidPrim(
            prim_path=f"/World/TrafficCone_{cone_idx}",
            name=f"TrafficCone_{cone_idx}",
            mass=500.0,
        )
        UsdPhysics.CollisionAPI.Apply(prim.prim)
        cone_idx += 1
        # right wall
        prims.create_prim(
            prim_path=f"/World/TrafficCone_{cone_idx}",
            position=(
                (problem_size / 2 - 0.5) * UNIT_SIZE,
                (problem_size / 2 - num_rack_long * 3 - 0.5 - i) * UNIT_SIZE,
                0
            ),
            orientation=euler_angles_to_quat([0, 0, 0]),
            scale=(0.01, 0.01, 0.01),
            usd_path=config["traffic_cone"]["url"],
            semantic_label=config["traffic_cone"]["class"],
        )
        prim = SingleRigidPrim(
            prim_path=f"/World/TrafficCone_{cone_idx}",
            name=f"TrafficCone_{cone_idx}",
            mass=500.0,
        )
        UsdPhysics.CollisionAPI.Apply(prim.prim)
        cone_idx += 1

    # Build inner objects
    for x in range(1, problem_size-1):
        for y in range(1, problem_size-1):
            position = (
                (x - problem_size / 2 + 0.5) * UNIT_SIZE,
                (-y + problem_size / 2 - 0.5) * UNIT_SIZE,
                0
            )
            if grid[x][y] == WALL:
                prims.create_prim(
                    prim_path=f"/World/TrafficCone_{cone_idx}",
                    position=position,
                    orientation=euler_angles_to_quat([0, 0, 0]),
                    scale=(0.02, 0.02, 0.02),
                    usd_path=config["traffic_cone"]["url"],
                    semantic_label=config["traffic_cone"]["class"],
                )
                prim = SingleRigidPrim(
                    prim_path=f"/World/TrafficCone_{cone_idx}",
                    name=f"TrafficCone_{cone_idx}",
                    mass=500.0,
                )
                UsdPhysics.CollisionAPI.Apply(prim.prim)
                cone_idx += 1
            elif grid[x][y] == HEAVY_OBJECT:
                prims.create_prim(
                    prim_path=f"/World/PlasticBox_{heavy_idx}",
                    position=position,
                    orientation=euler_angles_to_quat([0, 0, 0]),
                    scale=(0.024, 0.024, 0.024),
                    usd_path=config["plastic_box"]["url"],
                    semantic_label=config["plastic_box"]["class"],
                )
                prim = SingleRigidPrim(
                        prim_path=f"/World/PlasticBox_{heavy_idx}",
                        name=f"PlasticBox_{heavy_idx}",
                        mass=100.0,
                )
                UsdPhysics.CollisionAPI.Apply(prim.prim)
                heavy_idx += 1
            elif grid[x][y] == LIGHT_OBJECT:
                prims.create_prim(
                    prim_path=f"/World/Cardbox_{light_idx}",
                    position=(position[0], position[1], 0.1*UNIT_SIZE),
                    orientation=euler_angles_to_quat([0, 0, 0]),
                    scale=(0.012, 0.012, 0.012),
                    usd_path=config["cardbox"]["url"],
                    semantic_label=config["cardbox"]["class"],
                )
                prim = SingleRigidPrim(
                        prim_path=f"/World/Cardbox_{light_idx}",
                        name=f"Cardbox_{light_idx}",
                        mass=20.0,
                )
                UsdPhysics.CollisionAPI.Apply(prim.prim)
                material_api = UsdPhysics.MaterialAPI.Apply(prim.prim)
                material_api.CreateDynamicFrictionAttr(100.0)
                material_api.CreateStaticFrictionAttr(100.0)
                prims.create_prim(
                    prim_path=f"/World/Pallet_{light_idx}",
                    position=position,
                    orientation=euler_angles_to_quat([0, 0, 0]),
                    scale=(0.009, 0.009, 0.009),
                    usd_path=config["pallet"]["url"],
                    semantic_label=config["pallet"]["class"],
                )
                pallet_prim = SingleRigidPrim(
                        prim_path=f"/World/Pallet_{light_idx}",
                        name=f"Pallet_{light_idx}",
                        mass=40.0,
                )
                pallet_child_prim = pallet_prim.prim.GetChild("SM_ExportPallet_A04_01")
                UsdPhysics.CollisionAPI.Apply(pallet_child_prim)
                collision_api = UsdPhysics.MeshCollisionAPI.Apply(pallet_child_prim)
                collision_api.GetApproximationAttr().Set("convexDecomposition")
                material_api = UsdPhysics.MaterialAPI.Apply(pallet_child_prim)
                material_api.CreateDynamicFrictionAttr(100.0)
                material_api.CreateStaticFrictionAttr(100.0)
                light_idx += 1
            elif grid[x][y] == GOAL:
                prims.create_prim(
                    prim_path="/World/Goal_0",
                    position=position,
                    orientation=euler_angles_to_quat([0, 0, 0]),
                    scale=(0.005, 0.005, 0.005),
                    usd_path=config["goal"]["url"],
                    semantic_label=config["goal"]["class"],
                )
            elif grid[x][y] == ROBOT:
                if robot_direction == "dirIsLeft":
                    orientation = euler_angles_to_quat([0, 0, math.pi])
                    init_drift = (0.3*UNIT_SIZE, 0)
                elif robot_direction == "dirIsDown":
                    orientation = euler_angles_to_quat([0, 0, math.pi/2])
                    init_drift = (0, 0.3*UNIT_SIZE)
                elif robot_direction == "dirIsRight":
                    orientation = euler_angles_to_quat([0, 0, 0])
                    init_drift = (-0.3*UNIT_SIZE, 0)
                elif robot_direction == "dirIsUp":
                    orientation = euler_angles_to_quat([0, 0, -math.pi/2])
                    init_drift = (0, -0.3*UNIT_SIZE)
                
                forklift_prim = prims.create_prim(
                    prim_path="/World/Forklift_0",
                    position=(position[0]+init_drift[0], position[1]+init_drift[1], 0),
                    orientation=orientation,
                    scale=(0.7, 0.7, 0.7),
                    usd_path=config["forklift"]["url"],
                    semantic_label=config["forklift"]["class"],
                )

                back_wheel_swivel_prim = forklift_prim.GetChild("back_wheel_joints").GetChild("back_wheel_swivel")
                back_wheel_swivel_revolute_joint = UsdPhysics.RevoluteJoint.Get(stage, back_wheel_swivel_prim.GetPrimPath())
                back_wheel_swivel_revolute_joint.GetLowerLimitAttr().Set(-90)
                back_wheel_swivel_revolute_joint.GetUpperLimitAttr().Set(90)

                lift_joint_prim = forklift_prim.GetChild("lift_joint")
                lift_joint_drive_api = UsdPhysics.DriveAPI.Get(lift_joint_prim, "linear")
                lift_joint_drive_api.GetTargetPositionAttr().Set(1.0)
                lift_joint_drive_api.GetStiffnessAttr().Set(10000)

                front_right_roller_prim = forklift_prim.GetChild("roller_joints").GetChild("front_right_roller")
                back_right_roller_prim = forklift_prim.GetChild("roller_joints").GetChild("back_right_roller")
                front_left_roller_prim = forklift_prim.GetChild("roller_joints").GetChild("front_left_roller")
                back_left_roller_prim = forklift_prim.GetChild("roller_joints").GetChild("back_left_roller")
                front_right_roller_drive_api = UsdPhysics.DriveAPI.Apply(front_right_roller_prim, "angular")
                front_right_roller_drive_api.GetDampingAttr().Set(10000)
                front_right_roller_drive_api.GetStiffnessAttr().Set(100)
                back_right_roller_drive_api = UsdPhysics.DriveAPI.Apply(back_right_roller_prim, "angular")
                back_right_roller_drive_api.GetDampingAttr().Set(10000)
                back_right_roller_drive_api.GetStiffnessAttr().Set(100)
                front_left_roller_drive_api = UsdPhysics.DriveAPI.Apply(front_left_roller_prim, "angular")
                front_left_roller_drive_api.GetDampingAttr().Set(10000)
                front_left_roller_drive_api.GetStiffnessAttr().Set(100)
                back_left_roller_drive_api = UsdPhysics.DriveAPI.Apply(back_left_roller_prim, "angular")
                back_left_roller_drive_api.GetDampingAttr().Set(10000)
                back_left_roller_drive_api.GetStiffnessAttr().Set(100)

    print(f"Saving frame {assets_root_path}/{WAREHOUSE_SIZE}x{WAREHOUSE_SIZE}_namo_{problem_size}_{problem_mode}_{problem_idx}.usd into disk...")
    save_stage(f"{assets_root_path}/{WAREHOUSE_SIZE}x{WAREHOUSE_SIZE}_namo_{problem_size}_{problem_mode}_{problem_idx}.usd")
    print(f"End Saving frame into disk...")

    print(f"Robot direction: {robot_direction}")

