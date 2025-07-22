import os
import time
os.environ["OMNI_KIT_ACCEPT_EULA"] = "YES"

from isaacsim import SimulationApp

# Create the SimulationApp instance
simulation_app = SimulationApp({"headless": False})

# from isaaclab.app import AppLauncher
# app_launcher = AppLauncher({"headless": False})
# simulation_app = app_launcher.app

from isaacsim.core.utils.stage import create_new_stage, get_current_stage
from isaacsim.core.api import World
from isaacsim.core.utils import prims
from pxr import UsdPhysics


test_forklift = False
if test_forklift:
    create_new_stage()
    world_settings = {"physics_dt": 1.0 / 60.0, "stage_units_in_meters": 1.0, "rendering_dt": 1.0 / 60.0}
    world = World(**world_settings)
    world.scene.add_default_ground_plane()
    stage = get_current_stage()

    assets_root_path = f"{os.getcwd()}/assets"

    config = {
        "forklift": {
            "url": f"{assets_root_path}/Collected_forklift_b/forklift_b.usd",
            "class": "Forklift",
        },
    }

    forklift_prim = prims.create_prim(
        prim_path="/World/Forklift_0",
        position=(0, 0, 0),
        usd_path=config["forklift"]["url"],
        semantic_label=config["forklift"]["class"],
    )
    back_wheel_swivel_prim = forklift_prim.GetChild("back_wheel_joints").GetChild("back_wheel_swivel")
    back_wheel_swivel_revolute_joint = UsdPhysics.RevoluteJoint.Get(stage, back_wheel_swivel_prim.GetPrimPath())
    back_wheel_swivel_revolute_joint.GetLowerLimitAttr().Set(-90)
    back_wheel_swivel_revolute_joint.GetUpperLimitAttr().Set(90)


    back_wheel_drive_prim = forklift_prim.GetChild("back_wheel_joints").GetChild("back_wheel_drive")
    back_wheel_swivel_prim = forklift_prim.GetChild("back_wheel_joints").GetChild("back_wheel_swivel")
    back_wheel_drive_drive_api = UsdPhysics.DriveAPI.Get(back_wheel_drive_prim, "angular")
    back_wheel_swivel_drive_api = UsdPhysics.DriveAPI.Get(back_wheel_swivel_prim, "angular")
    back_wheel_swivel_drive_api.GetTargetPositionAttr().Set(90)
    back_wheel_drive_drive_api.GetTargetVelocityAttr().Set(-10)


    lift_joint_prim = forklift_prim.GetChild("lift_joint")
    lift_joint_drive_api = UsdPhysics.DriveAPI.Get(lift_joint_prim, "linear")
    lift_joint_drive_api.GetTargetPositionAttr().Set(0.8)

    front_right_roller_prim = forklift_prim.GetChild("roller_joints").GetChild("front_right_roller")
    back_right_roller_prim = forklift_prim.GetChild("roller_joints").GetChild("back_right_roller")
    front_left_roller_prim = forklift_prim.GetChild("roller_joints").GetChild("front_left_roller")
    back_left_roller_prim = forklift_prim.GetChild("roller_joints").GetChild("back_left_roller")

    roller_speed = 2000
    front_right_roller_drive_api = UsdPhysics.DriveAPI.Apply(front_right_roller_prim, "angular")
    front_right_roller_drive_api.GetTargetVelocityAttr().Set(roller_speed)
    front_right_roller_drive_api.GetDampingAttr().Set(10000)
    front_right_roller_drive_api.GetStiffnessAttr().Set(100)
    back_right_roller_drive_api = UsdPhysics.DriveAPI.Apply(back_right_roller_prim, "angular")
    back_right_roller_drive_api.GetTargetVelocityAttr().Set(roller_speed)
    back_right_roller_drive_api.GetDampingAttr().Set(10000)
    back_right_roller_drive_api.GetStiffnessAttr().Set(100)
    front_left_roller_drive_api = UsdPhysics.DriveAPI.Apply(front_left_roller_prim, "angular")
    front_left_roller_drive_api.GetTargetVelocityAttr().Set(-roller_speed)
    front_left_roller_drive_api.GetDampingAttr().Set(10000)
    front_left_roller_drive_api.GetStiffnessAttr().Set(100)
    back_left_roller_drive_api = UsdPhysics.DriveAPI.Apply(back_left_roller_prim, "angular")
    back_left_roller_drive_api.GetTargetVelocityAttr().Set(-roller_speed)
    back_left_roller_drive_api.GetDampingAttr().Set(10000)
    back_left_roller_drive_api.GetStiffnessAttr().Set(100)

try:
    # Loop while the simulation is running
    while simulation_app.is_running():
        simulation_app.update()
        time.sleep(0.01)
except KeyboardInterrupt:
    # Allow graceful shutdown on Ctrl+C
    pass
finally:
    simulation_app.close()
