import os
os.environ["OMNI_KIT_ACCEPT_EULA"] = "YES"

import math
import random
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

    rack_long_empty_prim = prims.create_prim(
        prim_path="/World/RackLongEmpty_0",
        position=(-0.5*UNIT_SIZE, 1.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, 0]),
        scale=(0.01, 0.01, 0.01),
        usd_path=config["rack_long_empty"]["url"],
        semantic_label=config["rack_long_empty"]["class"],
    )
    rack_long_empty_prim = prims.create_prim(
        prim_path="/World/RackLongEmpty_1",
        position=(-1.5*UNIT_SIZE, 3.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, math.pi/2]),
        scale=(0.01, 0.01, 0.01),
        usd_path=config["rack_long_empty"]["url"],
        semantic_label=config["rack_long_empty"]["class"],
    )
    rack_long_empty_prim = prims.create_prim(
        prim_path="/World/RackLongEmpty_2",
        position=(1.5*UNIT_SIZE, 3.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, math.pi/2]),
        scale=(0.01, 0.01, 0.01),
        usd_path=config["rack_long_empty"]["url"],
        semantic_label=config["rack_long_empty"]["class"],
    )
    rack_long_empty_prim = prims.create_prim(
        prim_path="/World/RackLongEmpty_3",
        position=(-1.5*UNIT_SIZE, -3.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, math.pi/2]),
        scale=(0.01, 0.01, 0.01),
        usd_path=config["rack_long_empty"]["url"],
        semantic_label=config["rack_long_empty"]["class"],
    )
    rack_long_empty_prim = prims.create_prim(
        prim_path="/World/RackLongEmpty_4",
        position=(1.5*UNIT_SIZE, -3.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, math.pi/2]),
        scale=(0.01, 0.01, 0.01),
        usd_path=config["rack_long_empty"]["url"],
        semantic_label=config["rack_long_empty"]["class"],
    )
    rack_long_empty_prim = prims.create_prim(
        prim_path="/World/RackLongEmpty_5",
        position=(-3.5*UNIT_SIZE, 1.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, 0]),
        scale=(0.01, 0.01, 0.01),
        usd_path=config["rack_long_empty"]["url"],
        semantic_label=config["rack_long_empty"]["class"],
    )
    rack_long_empty_prim = prims.create_prim(
        prim_path="/World/RackLongEmpty_6",
        position=(3.5*UNIT_SIZE, 1.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, 0]),
        scale=(0.01, 0.01, 0.01),
        usd_path=config["rack_long_empty"]["url"],
        semantic_label=config["rack_long_empty"]["class"],
    )
    rack_long_empty_prim = prims.create_prim(
        prim_path="/World/RackLongEmpty_7",
        position=(-3.5*UNIT_SIZE, -1.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, 0]),
        scale=(0.01, 0.01, 0.01),
        usd_path=config["rack_long_empty"]["url"],
        semantic_label=config["rack_long_empty"]["class"],
    )
    rack_long_empty_prim = prims.create_prim(
        prim_path="/World/RackLongEmpty_8",
        position=(3.5*UNIT_SIZE, -1.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, 0]),
        scale=(0.01, 0.01, 0.01),
        usd_path=config["rack_long_empty"]["url"],
        semantic_label=config["rack_long_empty"]["class"],
    )

    metal_fencing_prim = prims.create_prim(
        prim_path="/World/MetalFencing_0",
        position=(-0.5*UNIT_SIZE, -1*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, math.pi/2]),
        scale=(0.01, 0.01, 0.01),
        usd_path=config["metal_fencing"]["url"],
        semantic_label=config["metal_fencing"]["class"],
    )

    cardbox_prim = prims.create_prim(
        prim_path="/World/Cardbox_0",
        position=(-0.5*UNIT_SIZE, -2.5*UNIT_SIZE, 0.1*UNIT_SIZE),
        orientation=euler_angles_to_quat([0, 0, 0]),
        scale=(0.012, 0.012, 0.012),
        usd_path=config["cardbox"]["url"],
        semantic_label=config["cardbox"]["class"],
    )
    cardbox_prim = SingleRigidPrim(
            prim_path="/World/Cardbox_0",
            name="Cardbox_0",
            mass=10.0,
    )
    UsdPhysics.CollisionAPI.Apply(cardbox_prim.prim)
    pallet_prim = prims.create_prim(
        prim_path="/World/Pallet_0",
        position=(-0.5*UNIT_SIZE, -2.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, 0]),
        scale=(0.007, 0.009, 0.009),
        usd_path=config["pallet"]["url"],
        semantic_label=config["pallet"]["class"],
    )
    pallet_prim = SingleRigidPrim(
            prim_path="/World/Pallet_0",
            name="Pallet_0",
            mass=50.0,
    )
    pallet_child_prim = pallet_prim.prim.GetChild("SM_ExportPallet_A04_01")
    UsdPhysics.CollisionAPI.Apply(pallet_child_prim)
    collision_api = UsdPhysics.MeshCollisionAPI.Apply(pallet_prim.prim.GetChild("SM_ExportPallet_A04_01"))
    collision_api.GetApproximationAttr().Set("convexDecomposition")


    goal_prim = prims.create_prim(
        prim_path="/World/Goal_0",
        position=(2.5*UNIT_SIZE, -2.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, 0]),
        scale=(0.005, 0.005, 0.005),
        usd_path=config["goal"]["url"],
        semantic_label=config["goal"]["class"],
    )

    plastic_box_prim = prims.create_prim(
        prim_path="/World/PlasticBox_0",
        position=(-1.5*UNIT_SIZE, -1.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, 0]),
        scale=(0.025, 0.025, 0.025),
        usd_path=config["plastic_box"]["url"],
        semantic_label=config["plastic_box"]["class"],
    )
    plastic_box_prim = SingleRigidPrim(
            prim_path="/World/PlasticBox_0",
            name="PlasticBox_0",
            mass=100.0,
    )
    UsdPhysics.CollisionAPI.Apply(plastic_box_prim.prim)

    plastic_box_prim = prims.create_prim(
        prim_path="/World/PlasticBox_1",
        position=(-0.5*UNIT_SIZE, -1.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, 0]),
        scale=(0.025, 0.025, 0.025),
        usd_path=config["plastic_box"]["url"],
        semantic_label=config["plastic_box"]["class"],
    )
    plastic_box_prim = SingleRigidPrim(
            prim_path="/World/PlasticBox_1",
            name="PlasticBox_1",
            mass=100.0,
    )
    UsdPhysics.CollisionAPI.Apply(plastic_box_prim.prim)

    plastic_box_prim = prims.create_prim(
        prim_path="/World/PlasticBox_2",
        position=(0.5*UNIT_SIZE, -1.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, 0]),
        scale=(0.025, 0.025, 0.025),
        usd_path=config["plastic_box"]["url"],
        semantic_label=config["plastic_box"]["class"],
    )
    plastic_box_prim = SingleRigidPrim(
            prim_path="/World/PlasticBox_2",
            name="PlasticBox_2",
            mass=100.0,
    )
    UsdPhysics.CollisionAPI.Apply(plastic_box_prim.prim)

    plastic_box_prim = prims.create_prim(
        prim_path="/World/PlasticBox_3",
        position=(0.5*UNIT_SIZE, -2.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, 0]),
        scale=(0.025, 0.025, 0.025),
        usd_path=config["plastic_box"]["url"],
        semantic_label=config["plastic_box"]["class"],
    )
    plastic_box_prim = SingleRigidPrim(
            prim_path="/World/PlasticBox_3",
            name="PlasticBox_3",
            mass=100.0,
    )
    UsdPhysics.CollisionAPI.Apply(plastic_box_prim.prim)

    traffic_cone_prim = prims.create_prim(
        prim_path="/World/TrafficCone_0",
        position=(-3.5*UNIT_SIZE, 3.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, 0]),
        scale=(0.01, 0.01, 0.01),
        usd_path=config["traffic_cone"]["url"],
        semantic_label=config["traffic_cone"]["class"],
    )
    traffic_cone_prim = prims.create_prim(
        prim_path="/World/TrafficCone_1",
        position=(3.5*UNIT_SIZE, 3.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, 0]),
        scale=(0.01, 0.01, 0.01),
        usd_path=config["traffic_cone"]["url"],
        semantic_label=config["traffic_cone"]["class"],
    )
    traffic_cone_prim = prims.create_prim(
        prim_path="/World/TrafficCone_2",
        position=(-3.5*UNIT_SIZE, -3.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, 0]),
        scale=(0.01, 0.01, 0.01),
        usd_path=config["traffic_cone"]["url"],
        semantic_label=config["traffic_cone"]["class"],
    )
    traffic_cone_prim = prims.create_prim(
        prim_path="/World/TrafficCone_3",
        position=(3.5*UNIT_SIZE, -3.5*UNIT_SIZE, 0),
        orientation=euler_angles_to_quat([0, 0, 0]),
        scale=(0.01, 0.01, 0.01),
        usd_path=config["traffic_cone"]["url"],
        semantic_label=config["traffic_cone"]["class"],
    )

    # Spawn a new forklift at a random pose
    forklift_prim = prims.create_prim(
        prim_path="/World/Forklift_0",
        position=(-1.5*UNIT_SIZE, 1.5*UNIT_SIZE, 0),
        # orientation=euler_angles_to_quat([0, 0, random.uniform(0, math.pi)]),
        orientation=euler_angles_to_quat([0, 0, math.pi/2]),
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

    print(f"Saving frame into disk...")
    save_stage(f"{assets_root_path}/{WAREHOUSE_SIZE}x{WAREHOUSE_SIZE}_namo_example.usd")
    print(f"End Saving frame into disk...")


